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
import javax.swing.UIManager;
import java.awt.DefaultKeyboardFocusManager;
import javax.swing.JPanel;

public class Fereastra extends JFrame{
    MainPanel mainpanel ;
    private static final long serialVersionUID = 1L;
    Applet container;
    
    public Fereastra(final boolean applet, Applet container){
        this.container = container;
        setTitle("Luxoft - Test Automation Framework");
//         System.out.println("Started Fereastra initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Started Frame initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();
        mainpanel = new MainPanel(applet);
//         JPanel p = new JPanel();
//         p.add();
        if(container!=null)container.add(mainpanel);
        else{
            setLayout(null);
            add(mainpanel);
            setBounds(0,60,mainpanel.getWidth()+30,mainpanel.getHeight()+45);
            addWindowListener(new WindowAdapter(){
                public void windowClosing(WindowEvent e){                
                    int r = JOptionPane.showConfirmDialog(mainpanel, "Save your Suite XML before exiting ?", "Save", JOptionPane.YES_NO_OPTION);
                    if(r == JOptionPane.OK_OPTION){mainpanel.saveUserXML();}
                    if(deleteTemp(new File(Repository.temp)))System.out.println(Repository.temp+System.getProperty("file.separator")+"Twister deleted successfull");
                    else System.out.println("Could not delete: "+Repository.temp+System.getProperty("file.separator")+"Twister");
                    dispose();
                    Repository.run = false;
                    if(!applet)System.exit(0);}});
            addComponentListener(new ComponentAdapter(){
                public void componentResized(ComponentEvent e){
                    if(Repository.frame!=null){
                        mainpanel.p2.splitPane.setSize(Repository.frame.getWidth()-52,Repository.frame.getHeight()-120);
                        mainpanel.p1.splitPane.setSize(Repository.frame.getWidth()-52,Repository.frame.getHeight()-120);
                        mainpanel.setSize(Repository.frame.getWidth()-28,Repository.frame.getHeight()-50);
                        mainpanel.p4.scroll.setSize(Repository.frame.getWidth()-310,Repository.frame.getHeight()-150);
                        mainpanel.p4.main.setSize(Repository.frame.getWidth()-300,Repository.frame.getHeight()-130);
                        mainpanel.p4.dut.setPreferredSize(new Dimension(getWidth()-300,getHeight()-150));
                        //Repository.frame.mainpanel.p5.nettop.setPreferredSize(new Dimension(getWidth()-50,672));
                    }}});
            setVisible(true);}
        Repository.intro.text = "Starting applet";
        Repository.intro.percent = 1;
        Repository.intro.repaint();
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