import java.applet.Applet; 
import javax.swing.JFrame;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.JOptionPane;
import java.io.File;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.Dimension;
import java.awt.Container;
import java.awt.Color;
import javax.swing.JDesktopPane;
import javax.swing.JInternalFrame;
import javax.swing.UIManager.*;
import javax.swing.UIManager;
import java.awt.DefaultKeyboardFocusManager;



public class Fereastra extends JFrame{
    MainPanel p ;
    private static final long serialVersionUID = 1L;
    Applet container;
    
    public Fereastra(final boolean applet, Applet container){
        this.container = container;
        setFocusTraversalKeysEnabled(false);
        setFocusTraversalPolicyProvider(false);
        setFocusCycleRoot(false);
        setFocusTraversalKeys(DefaultKeyboardFocusManager.BACKWARD_TRAVERSAL_KEYS,null);
        setFocusTraversalKeys(DefaultKeyboardFocusManager.DOWN_CYCLE_TRAVERSAL_KEYS,null);
        setFocusTraversalKeys(DefaultKeyboardFocusManager.FORWARD_TRAVERSAL_KEYS,null);
        setFocusTraversalKeys(DefaultKeyboardFocusManager.UP_CYCLE_TRAVERSAL_KEYS,null);
        
//         try{
//             for (LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
//                 System.out.println("Look and feel: "+info.getName());
//                 if ("Nimbus".equals(info.getName())) {
//                     UIManager.setLookAndFeel(info.getClassName());
//                     break;}}}
//          catch (Exception e) {
//             // If Nimbus is not available, you can set the GUI to another look and feel.
//         }
        
        
        setTitle("Luxoft - Test Automation Framework");
//         System.out.println("Started Fereastra initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Started Frame initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();
        p = new MainPanel(applet);
        setLayout(null);
        add(p);
        setBounds(0,60,p.getWidth()+30,p.getHeight()+45);
        addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent e){                
                int r = JOptionPane.showConfirmDialog(p, "Save your Suite XML before exiting ?", "Save", JOptionPane.YES_NO_OPTION);
                if(r == JOptionPane.OK_OPTION){p.saveUserXML();}
                if(deleteTemp(new File(Repository.temp+System.getProperty("file.separator")+"Twister")))System.out.println(Repository.temp+System.getProperty("file.separator")+"Twister deleted successfull");
                else System.out.println("Could not delete: "+Repository.temp+System.getProperty("file.separator")+"Twister");
                dispose();
                Repository.run = false;
                if(!applet)System.exit(0);}});
        addComponentListener(new ComponentAdapter(){
            public void componentResized(ComponentEvent e){
                if(Repository.f!=null){
                    p.p2.splitPane.setSize(Repository.f.getWidth()-52,Repository.f.getHeight()-120);
                    p.p1.splitPane.setSize(Repository.f.getWidth()-52,Repository.f.getHeight()-120);
                    p.setSize(Repository.f.getWidth()-28,Repository.f.getHeight()-50);
                    p.p3.pane.setSize(Repository.f.getWidth()-42,Repository.f.getHeight()-82);
                    p.p4.scroll.setSize(Repository.f.getWidth()-310,Repository.f.getHeight()-150);
                    p.p4.main.setSize(Repository.f.getWidth()-300,Repository.f.getHeight()-130);}}});
        Repository.intro.text = "Starting applet";
        Repository.intro.percent = 1;
        Repository.intro.repaint();
        if(container!=null)container.add(p);
        else setVisible(true);
        Repository.intro.dispose();
//         System.out.println("Finished Fereastra initialization: "+System.currentTimeMillis());
    }
    
    public static boolean deleteTemp(File dir){    
        if (dir.isDirectory()){
            String[] children = dir.list();
            for (int i=0; i<children.length; i++) {
                boolean success = deleteTemp(new File(dir, children[i])); 
                if(success) System.out.println("successfull");
                else System.out.println("failed");
                if (!success) {return false;}}}
        try{System.out.print("Deleting "+dir.getCanonicalPath()+"....");}
        catch(Exception e){e.printStackTrace();}
        return dir.delete();}}