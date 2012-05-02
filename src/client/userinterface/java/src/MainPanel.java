import java.io.File;
import java.io.PrintStream;
import javax.swing.JOptionPane;
import javax.swing.JTabbedPane;
import java.awt.Dimension;
import java.awt.Toolkit;
import javax.swing.ImageIcon;
import javax.swing.event.ChangeListener;
import javax.swing.event.ChangeEvent;
import java.awt.DefaultKeyboardFocusManager;
import javax.swing.InputMap; 
import javax.swing.JComponent;
import javax.swing.KeyStroke;
import java.awt.event.KeyEvent;
import java.awt.event.InputEvent;
import java.net.URL;
import javax.swing.JScrollPane;
import javax.swing.SwingUtilities;

public class MainPanel extends JTabbedPane{
    private static final long serialVersionUID = 1L;
    public Panel1 p1;
    public Panel2 p2;
    public Panel4 p4;
/*     public Panel5 p5;*/
    private boolean applet;

    public MainPanel(boolean applet){
        InputMap map = getInputMap(JComponent.WHEN_ANCESTOR_OF_FOCUSED_COMPONENT);
        KeyStroke keyStroke = KeyStroke.getKeyStroke(KeyEvent.VK_UP, InputEvent.CTRL_MASK, false );
        map.put( keyStroke, "DoNothing" ); 
//         System.out.println("Started MainPanel initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Started Main initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        this.applet = applet;
        p1 = new Panel1("", applet,(int)screenSize.getWidth());
        p2 = new Panel2(applet);    
        p4 = new Panel4();         
/*         p5 = new Panel5(1500,612);*/
        setBounds(5, 5, (int)screenSize.getWidth()-50, 672);
        addTab("Suites", new ImageIcon(), p1);
        add("Monitoring", p2);
        add("Reports", null);
        add("Configuration", p4);
/*         add("Network", new JScrollPane(p5));*/
        new Thread(){
            public void run(){
                
                SwingUtilities.invokeLater(new Runnable() { 
                    public void run(){
                        try{
                            while(p1.sc.g.getGraphics() == null) 
                                try{Thread.sleep(100);}
                                catch(Exception e){System.out.println("Thread interrupted at getting Graphics");}
                            File usersdirectory = new File(Repository.getUsersDirectory());
                            String users[] = new String[usersdirectory.list().length + 1];
                            System.arraycopy(usersdirectory.list(), 0, users, 0, usersdirectory.list().length);
                            users[users.length - 1] = "New File";
                            String user = (String)JOptionPane.showInputDialog(p1, "Select Suite file", "Suite File", 1, null, users, "Suite File");
                            if(user.equals("New File")){
                                user = JOptionPane.showInputDialog(null, "Please enter file name", "File Name", -1).toUpperCase();
                                (new XMLBuilder(Repository.getSuite())).writeXMLFile((new StringBuilder()).append(Repository.getUsersDirectory()).append(Repository.getBar()).append(user).append(".XML").toString(),false);
                                p1.sc.g.setUser((new StringBuilder()).append(Repository.getUsersDirectory()).append(Repository.getBar()).append(user).append(".XML").toString());
                                p1.sc.g.printXML(p1.sc.g.getUser(),false,false);}
                            else if(user != null){
                                p1.sc.g.setUser((new StringBuilder()).append(Repository.getUsersDirectory()).append(Repository.getBar()).append(user).toString());
                                p1.sc.g.parseXML(new File((new StringBuilder()).append(Repository.getUsersDirectory()).append(Repository.getBar()).append(user).toString()));}}
                        catch(NullPointerException e){}}});}}.start();
        if(applet){
            addChangeListener(new ChangeListener(){
                public void stateChanged(ChangeEvent e){
                    if(getSelectedIndex()==2){
                        try{Repository.frame.container.getAppletContext().showDocument(new URL("http://"+Repository.host+":"+Repository.getHTTPServerPort()), "_blank");}
                        catch(Exception ex){ex.printStackTrace();}
                        setSelectedIndex(1);}}});}
        Repository.intro.text = "Finished Main initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();}
 
    public void saveUserXML(){
        if(!p1.sc.g.getUser().equals("")){
            p1.sc.g.printXML(p1.sc.g.getUser(), false,false);}}}