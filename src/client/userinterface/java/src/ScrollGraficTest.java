import javax.swing.JPanel;
import java.awt.ScrollPane;
import javax.swing.JScrollPane;
import java.awt.Color;

public class ScrollGraficTest extends JPanel{ 
    private static final long serialVersionUID = 1L;
    JScrollPane pane;
    GraficTest g;
    
    public ScrollGraficTest(int x, int y,boolean applet){
        g = new GraficTest(0,0,applet);
        pane = new JScrollPane(g);
        pane.getVerticalScrollBar().setUnitIncrement(16);
        add(pane);}}