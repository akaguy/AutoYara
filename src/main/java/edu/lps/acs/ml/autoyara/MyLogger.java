package edu.lps.acs.ml.autoyara;

import org.slf4j.LoggerFactory;
import org.slf4j.Logger;

public class MyLogger{

    private static Logger logger;
    private MyLogger(){
    }
    public synchronized static Logger getLogger()
    {
        if (logger!= null)
            return logger;
        return logger= LoggerFactory.getLogger("Logger");
    }

}