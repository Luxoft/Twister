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
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Toolkit;
import javax.swing.JLabel;

/*
 * main window displayed if twister is running local
 */
public class Window extends JFrame{
    MainPanel mainpanel;//applet main container
    private static final long serialVersionUID = 1L;
    Applet container;
    JPanel appletpanel;
    
    /*
     * applet - true if starts from applet, false otherwie
     * container - if not null, applet container
     */
   
    public Window(final boolean applet, Applet container){
        this.container = container;
        setTitle("Luxoft - Test Automation Framework");
        Repository.intro.setStatus("Started Frame initialization");
        Repository.intro.addPercent(0.035);
        Repository.intro.repaint();
        mainpanel = new MainPanel(applet);
        if(container!=null){
            appletpanel = new JPanel();
            Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
            appletpanel.setBounds(5, 5, (int)screenSize.getWidth(), 672);
            appletpanel.setBackground(Color.WHITE);
            appletpanel.setLayout(null);
            appletpanel.add(mainpanel);
            container.add(appletpanel);}
        else{
            setLayout(null);
            add(mainpanel);
            setBounds(0,60,mainpanel.getWidth()+30,mainpanel.getHeight()+45);
            addWindowListener(new WindowAdapter(){
                public void windowClosing(WindowEvent e){                
//                     int r = JOptionPane.showConfirmDialog(mainpanel, "Save your Suite XML before exiting ?", "Save", JOptionPane.YES_NO_OPTION);
                    int r = (Integer)CustomDialog.showDialog(new JLabel("Save your Suite XML before exiting ?"), JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION, mainpanel, "Save", null);
                    if(r == JOptionPane.OK_OPTION){mainpanel.saveUserXML();}
                    if(deleteTemp(new File(Repository.temp)))System.out.println(Repository.temp+System.getProperty("file.separator")+"Twister deleted successfull");
                    else System.out.println("Could not delete: "+Repository.temp+System.getProperty("file.separator")+"Twister");
                    dispose();
                    Repository.run = false;
                    if(!applet)System.exit(0);}});
            addComponentListener(new ComponentAdapter(){
                public void componentResized(ComponentEvent e){
                    if(Repository.window!=null){
                        mainpanel.p2.splitPane.setSize(Repository.window.getWidth()-52,Repository.window.getHeight()-120);
                        mainpanel.p1.splitPane.setSize(Repository.window.getWidth()-52,Repository.window.getHeight()-120);
                        mainpanel.setSize(Repository.window.getWidth()-28,Repository.window.getHeight()-50);
                        mainpanel.p4.scroll.setSize(Repository.window.getWidth()-310,Repository.window.getHeight()-150);
                        mainpanel.p4.main.setSize(Repository.window.getWidth()-300,Repository.window.getHeight()-130);
                        mainpanel.p4.dut.setPreferredSize(new Dimension(getWidth()-300,getHeight()-150));
                        //Repository.window.mainpanel.p5.nettop.setPreferredSize(new Dimension(getWidth()-50,672));
                    }}});
            setVisible(true);}
        Repository.intro.setStatus("Starting applet");
        Repository.intro.addPercent(1);
        Repository.intro.repaint();
        Repository.intro.dispose();}
    
    /*
     * static method used to dele a directory 
     * dir - the directory to be deleted localy
     */
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