from opentracing_instrumentation import traced_function

class abc(object):
    
    @traced_function(name="update")
    @classmethod
    def update(cls, id,**kwargs):
        print("update")
 
 if __name__ == "__main__":
     abc.update(1)





