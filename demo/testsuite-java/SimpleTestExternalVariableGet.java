
// simple test external variable get




import junit.framework.*;

import tscJython.utilities.ExternalVariableFactory;
import tscJython.interfaces.ExternalVariableType;

import org.python.core.PyObject;




public class SimpleTestExternalVariableGet extends TestCase {

    public SimpleTestExternalVariableGet(String name) {
        super(name);
    }


    public void testSimpleTestExternalVariableGet() {
        ExternalVariableFactory externalVariableFactory = new ExternalVariableFactory();
        ExternalVariableType externalVariable = externalVariableFactory.create();

        String variableName = "testvar";
        PyObject response = externalVariable.getVariable(variableName);
        System.out.println("external variable get response: " + variableName + " = " + response);
    }

}

