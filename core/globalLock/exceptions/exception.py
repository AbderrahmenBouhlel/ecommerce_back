

class LockError(Exception): pass





class LockNotFoundError(LockError): pass
class LockAcquisitionError(LockError): pass
class LockCreationError(LockError): pass

