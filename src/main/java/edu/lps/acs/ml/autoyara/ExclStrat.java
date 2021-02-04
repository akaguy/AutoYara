package edu.lps.acs.ml.autoyara;

import com.google.gson.ExclusionStrategy;
import com.google.gson.FieldAttributes;

/**
 * @author edraff
 */

public class ExclStrat implements ExclusionStrategy {

    public boolean shouldSkipClass(Class<?> arg0) {
        return false;
    }

    public boolean shouldSkipField(FieldAttributes f) {

        return (f.getName().equals("coverage") || f.getName().contains("Comment"));
    }

}
