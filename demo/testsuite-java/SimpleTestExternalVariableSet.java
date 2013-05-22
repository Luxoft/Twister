
// simple test external variable set




import junit.framework.*;

import tscJython.utilities.ExternalVariableFactory;
import tscJython.interfaces.ExternalVariableType;




public class SimpleTestExternalVariableSet extends TestCase {

    public SimpleTestExternalVariableSet(String name) {
        super(name);
    }


    public void testSimpleTestExternalVariableSet() {
        ExternalVariableFactory externalVariableFactory = new ExternalVariableFactory();
        ExternalVariableType externalVariable = externalVariableFactory.create();

        String variableName = "testvar";
        int variableValue = 42;
        boolean response = externalVariable.setVariable(variableName, variableValue);
        System.out.println("external variable set response: " + response);
        if (response) {
            System.out.println("external variable set: " + variableName + " = " + variableValue);
        }
    }

}

