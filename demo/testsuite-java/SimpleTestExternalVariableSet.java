
// simple test external variable set




import junit.framework.*;

import tscJython.utilities.ExternalVariableFactory;
import tscJython.interfaces.ExternalVariableType;

import org.python.core.Py;
import java.util.HashMap;
import java.util.Map;




public class SimpleTestExternalVariableSet extends TestCase {

    public SimpleTestExternalVariableSet(String name) {
        super(name);
    }


    public void testSimpleTestExternalVariableSet() {
        ExternalVariableFactory externalVariableFactory = new ExternalVariableFactory();
        ExternalVariableType externalVariable = externalVariableFactory.create();

        boolean response;

        int testVarInteger = 42;
        response = externalVariable.setVariable("testVarInteger", Py.java2py(testVarInteger));
        System.out.println("external variable set testVarInteger response: " + response);

        int[] testVarList = {42, 44};
        response = externalVariable.setVariable("testVarList", Py.java2py(testVarList));
        System.out.println("external variable set testVarList response: " + response);

        Map testVarHashMap = new HashMap();
        testVarHashMap.put("key", 42);
        response = externalVariable.setVariable("testVarHashMap", Py.java2py(testVarHashMap));
        System.out.println("external variable set testVarHashMap response: " + response);
    }
}

