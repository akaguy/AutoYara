package edu.lps.acs.ml.autoyara;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class YaraRulesContainer {

    List<YaraRuleContainerConjunctive> signature_sets = new ArrayList<>();

    public YaraRulesContainer()
    {
    }

    public YaraRulesContainer(List<YaraRuleContainerConjunctive> rules){
        this.signature_sets = rules;
    }

    public void addRule(YaraRuleContainerConjunctive yara)
    {
        this.signature_sets.add(yara);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for(var rule:signature_sets){
            sb.append(rule.toString()).append('\n');
        }
        return sb.toString();
    }

    public int minConjunctionSize()
    {
        return signature_sets.stream().mapToInt(s->s.minConjunctionSize()).min().orElse(0);
    }

    public boolean match(InputStream input){
        return signature_sets.stream().anyMatch(s->s.match(input));
    }
}
