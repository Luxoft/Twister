
// simple test




import junit.framework.*;




public class SimpleTest extends TestCase {

    public SimpleTest(String name) {
        super(name);
    }


    public void testSimpleTest() {
        int answer = 2;
        assertEquals((1+1), answer);

        System.out.println("java simple test print");
    }

}

