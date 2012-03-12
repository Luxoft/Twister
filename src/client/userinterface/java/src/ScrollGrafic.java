import javax.swing.JPanel;
import java.awt.ScrollPane;
import javax.swing.JScrollPane;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.DefaultKeyboardFocusManager;

public class ScrollGrafic extends JPanel{
    private static final long serialVersionUID = 1L;
    public JScrollPane pane;
    public Grafic g;
    
    public ScrollGrafic(int x, int y,TreeDropTargetListener tdtl, String user,boolean applet){
        setFocusTraversalKeysEnabled(false);
        setFocusTraversalPolicyProvider(false);
        setFocusCycleRoot(false);
        setFocusTraversalKeys(DefaultKeyboardFocusManager.BACKWARD_TRAVERSAL_KEYS,null);
        setFocusTraversalKeys(DefaultKeyboardFocusManager.DOWN_CYCLE_TRAVERSAL_KEYS,null);
        setFocusTraversalKeys(DefaultKeyboardFocusManager.FORWARD_TRAVERSAL_KEYS,null);
        setFocusTraversalKeys(DefaultKeyboardFocusManager.UP_CYCLE_TRAVERSAL_KEYS,null);
//         System.out.println("Started ScrollGrafic initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Started Users Graphics initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();
        g = new Grafic(tdtl,user);
        pane = new JScrollPane(g);
        pane.setFocusTraversalKeysEnabled(false);
        pane.setFocusTraversalPolicyProvider(false);
        pane.setFocusCycleRoot(false);
        pane.setFocusTraversalKeys(DefaultKeyboardFocusManager.BACKWARD_TRAVERSAL_KEYS,null);
        pane.setFocusTraversalKeys(DefaultKeyboardFocusManager.DOWN_CYCLE_TRAVERSAL_KEYS,null);
        pane.setFocusTraversalKeys(DefaultKeyboardFocusManager.FORWARD_TRAVERSAL_KEYS,null);
        pane.setFocusTraversalKeys(DefaultKeyboardFocusManager.UP_CYCLE_TRAVERSAL_KEYS,null);
        pane.setMinimumSize(new Dimension(100,350));
        pane.setMaximumSize(new Dimension(1000,1000));
        pane.setPreferredSize(new Dimension(450,500));
        pane.getVerticalScrollBar().setUnitIncrement(16);
        add(pane);
//         System.out.println("Finished ScrollGrafic initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Finished Users Graphics initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();}}