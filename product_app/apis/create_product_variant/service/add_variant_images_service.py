import datetime
from typing import List
import uuid
import mimetypes
import os

from django.core.files.storage import default_storage


from django.db import OperationalError
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException

from product_app.models import ProductVariant, ProductVariantImage
from django.core.files.uploadedfile import UploadedFile

from django.db import transaction

from config.settings import MEDIA_URL

class AddVariantImagesService:
    
    
    def excute(self , variant: ProductVariant , images: list[UploadedFile]) -> List[ProductVariantImage]:
        
        created_variant_images: List[ProductVariantImage] = []
        
        # relative paths (in the MEDIA_ROOT storage)
        stored_images_paths: List[str] = []
        
        
        try:
            # products/UUYHS568/variants/PV_UZH55/
            relative_folder = os.path.join('products', str(variant.product.id), 'variants', str(variant.id))
        
            for image in images:
                #1 - genrate unique file name and save the file to the storage path
                safe_relative_file_path = self.__save_image_file(image, relative_folder)
                stored_images_paths.append(safe_relative_file_path)
                
                #2 - genrate the full URL path for the image
                image_url = f"{MEDIA_URL.rstrip('/')}/{safe_relative_file_path}"
                
                #3 - create a ProductVariantImage record in the database
                productVariantImage: ProductVariantImage = self.__create_variant_image_record(variant, image_url)
                created_variant_images.append(productVariantImage)
            
            return created_variant_images
        
        except Exception as e:
            self.__delete_saved_files(stored_images_paths)
            raise e
    
    
    
    def __delete_saved_files(self, stored_images_paths: List[str]):
        for relative_path in stored_images_paths:
            try:
                default_storage.delete(relative_path)
            except Exception as cleanup_exception:
                # Log the cleanup failure but do not raise, since we want to preserve the original exception
                print(f"Failed to clean up file at {relative_path}: {cleanup_exception}")
                
    def __create_variant_image_record(self, variant: ProductVariant, image_url: str) -> ProductVariantImage:
        try:
            last_image = ProductVariantImage.objects.filter(product_variant=variant).order_by("order").last()
            next_order = last_image.order + 1 if last_image else 0
            
            return ProductVariantImage.objects.create(
                product_variant=variant,
                image_url=image_url,
                order=next_order
            )
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
    
    
    # in case of success storing it will return the relative path to the stored file, e.g. 'products/1/variants/2/unique_name.jpg'
    def __save_image_file(self, image: UploadedFile, relative_folder: str):
        try:
            relative_path = self.__generate_image_relative_path(relative_folder, image)
            # relative_path should be 'products/1/variants/2/unique_name.jpg'
            # default_storage handles the MEDIA_ROOT joining and permission checks
            path = default_storage.save(relative_path, image)
            return path
        except OSError as e:
            if e.errno == 28:
                raise ServerUnavailableException(message="Storage is full.", cause=e)
            raise InternalServerErrorException(message="FileSystem error.", cause=e)
            
            
    # todo : in the next version use tools like pillow to validate the file content to be a real image and not just rely on the content type sent by the client, which can be easily faked. 
    def __generate_image_relative_path(self, relative_folder: str, image_file: UploadedFile) -> str:
        # 1. Get the extension based on Content-Type (MIME type)
        # This ignores the .jpg or .png in the actual filename and looks at the file data
        content_type = image_file.content_type  # e.g., 'image/jpeg'
        extension = mimetypes.guess_extension(content_type) or '.jpg'

        # 2. Generate timestamp (format: 20260429_141500)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # 3. Generate a short UUID for brevity (or full if you prefer)
        unique_id = uuid.uuid4().hex[:8]

        # 4. Final name: 20260429_141500_a1b2c3d4.jpg
        unique_filename = f"{timestamp}_{unique_id}{extension}"
        
        relative_file_path = os.path.join(relative_folder, unique_filename)
        
        return relative_file_path
    