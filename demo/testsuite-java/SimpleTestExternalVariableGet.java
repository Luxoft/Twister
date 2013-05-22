
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

        PyObject testVarInteger = externalVariable.getVariable("testVarInteger");
        testVarInteger = (PyObject)testVarInteger.__tojava__(PyObject.class);
        System.out.println("external variable testVarInteger get response: " + testVarInteger);

        PyObject testVarList = externalVariable.getVariable("testVarList");
        testVarList = (PyObject)testVarList.__tojava__(PyObject.class);
        System.out.println("external variable testVarList get response: " + testVarList);

        PyObject testVarHashMap = externalVariable.getVariable("testVarHashMap");
        testVarHashMap = (PyObject)testVarHashMap.__tojava__(PyObject.class);
        System.out.println("external variable testVarList get response: " + testVarHashMap);

        PyObject testVarSet = externalVariable.getVariable("testVarSet");
        testVarSet = (PyObject)testVarSet.__tojava__(PyObject.class);
        System.out.println("external variable testVarList get response: " + testVarSet);
    }
}

