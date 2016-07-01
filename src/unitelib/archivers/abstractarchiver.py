import abc


class AbstractArchiver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list_contents(self, opts):
        raise NotImplementedError()

    @abc.abstractmethod
    def extract_archive(self, opts):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def create_archive(self, opts):
        raise NotImplementedError()
