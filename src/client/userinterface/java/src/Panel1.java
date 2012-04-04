import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import javax.swing.JPanel;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import java.awt.dnd.DropTargetListener;
import java.awt.dnd.DropTargetDragEvent;
import java.awt.dnd.DropTargetEvent;
import java.awt.dnd.DropTargetDropEvent;
import javax.swing.JSplitPane;
import java.awt.Dimension;
import javax.swing.JScrollPane;
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeEvent; 
import javax.swing.JButton;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Toolkit;
import javax.swing.JDesktopPane;
import javax.swing.JInternalFrame;
import java.awt.Container;
import java.awt.DefaultKeyboardFocusManager;
import javax.swing.JLabel;
import javax.swing.JFileChooser;


public class Panel1 extends JPanel{
    private static final long serialVersionUID = 1L;
    public ScrollGrafic sc;
    public ExplorerPanel ep;
    private TreeDropTargetListener tdtl;
    private boolean applet;
    public JSplitPane splitPane;    
    public SuitaDetails suitaDetails;
    private JLabel openedfile;
    
    public Panel1(String user, final boolean applet, int width){
//         System.out.println("Started Panel1 initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Started Suites interface initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();
        openedfile = new JLabel();
        openedfile.setBounds(210,23,250,20);
        add(openedfile);
        JButton addsuite = new JButton("Add Suite");
        addsuite.setBounds(10,23,100,20);
        add(addsuite);
        addsuite.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.addSuiteFromButton();}});
        JButton generate = new JButton("Generate");
        generate.setBounds(115,23,90,20);
        add(generate);
        suitaDetails = new SuitaDetails(Repository.getDatabaseUserFields());
        generate.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String result="";
                try{result = (String)Repository.frame.mainpanel.p2.client.execute("getExecStatusAll",new Object[]{});}
                catch(Exception e){System.out.println("Could not connect to server");}
                int defsNr = suitaDetails.getDefsNr();
                boolean execute=true;
                for(int i=0;i<Repository.getSuiteNr();i++){
                    if(Repository.getSuita(i).getUserDefNr()<defsNr){
                        JOptionPane.showMessageDialog(Repository.frame, "Please set user defined fields for: "+Repository.getSuita(i).getName());
                        execute = false;
                        break;}
                    for(int j=0;j<defsNr;j++){
                        if(Repository.getSuita(i).getUserDef(j)[1].length()==0&&Repository.getDatabaseUserFields().get(j)[Repository.MANDATORY].equals("true")){
                            JOptionPane.showMessageDialog(Repository.frame, "Please set user defined field at "+Repository.getDatabaseUserFields().get(j)[Repository.LABEL]+" for: "+Repository.getSuita(i).getName());
                            execute = false;
                            break;}}
                    if(!execute)break;}                
                if(execute){
                    if(!result.equals("running")){
                        sc.g.printXML(Repository.getTestXMLDirectory(),true,false);
                        Repository.emptyTestRepository();
                        File xml = new File(Repository.getTestXMLDirectory());    
                        int size = Repository.logs.size();
                        for(int i=5;i<size;i++){Repository.logs.remove(5);}
                        new XMLReader(xml).parseXML(sc.g.getGraphics(), true);
                        Repository.frame.mainpanel.p2.updateTabs();
                        JOptionPane.showMessageDialog(Repository.frame, "File successfully generated ");}
                    else{JOptionPane.showMessageDialog(Repository.frame, "Please close Central Engine before generating");}}}});
        this.applet = applet;
        JMenuBar menu = new JMenuBar();
        menu.setLayout(null);
        menu.setBounds(0, 0, width, 20);
        JMenu filemenu = new JMenu("File");
        filemenu.setBounds(10,0,40,20);
        JMenuItem newuser = new JMenuItem("New suite file");
        newuser.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String user ="";
                Repository.emptyRepository();
                try{user = JOptionPane.showInputDialog(null, "Please enter file name", "File Name", -1).toUpperCase();}
                catch(NullPointerException e){}
                (new XMLBuilder(Repository.getSuite())).writeXMLFile(Repository.getUsersDirectory()+System.getProperty("file.separator")+user+".xml",false);
                Repository.frame.mainpanel.p1.sc.g.setUser(Repository.getUsersDirectory()+System.getProperty("file.separator")+user+".xml");
                sc.g.printXML(sc.g.getUser(),false,false);
                sc.g.updateScroll();
                sc.g.repaint();}});
        filemenu.add(newuser);
        JMenuItem changeuser = new JMenuItem("Open suite file");
        changeuser.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                File usersdirectory = new File(Repository.getUsersDirectory());
//                 String users[] = new String[usersdirectory.list().length + 1];
                String users[] = new String[usersdirectory.list().length];
                System.arraycopy(usersdirectory.list(), 0, users, 0, usersdirectory.list().length);
//                 users[users.length - 1] = "New File";
                String user = (String)JOptionPane.showInputDialog(null, "Select suite file", "Suite File", 1, null, users, "Suite File");
//                 if(user!=null && user.equals("New File")){
//                     Repository.emptyRepository();
//                     try{user = JOptionPane.showInputDialog(null, "Please enter file name", "File Name", -1).toUpperCase();}
//                     catch(NullPointerException e){}
//                     (new XMLBuilder(Repository.getSuite())).writeXMLFile(Repository.getUsersDirectory()+System.getProperty("file.separator")+user+".xml",false);
//                     Repository.frame.mainpanel.p1.sc.g.setUser(Repository.getUsersDirectory()+System.getProperty("file.separator")+user+".xml");
//                     sc.g.printXML(sc.g.getUser(),false,false);
//                     sc.g.updateScroll();}
//                 else 
                if(user != null){
                    Repository.emptyRepository();
                    Repository.frame.mainpanel.p1.sc.g.setUser(Repository.getUsersDirectory()+Repository.getBar()+user);
                    Repository.frame.mainpanel.p1.sc.g.parseXML(new File(Repository.getUsersDirectory()+System.getProperty("file.separator")+user));}
                if(Repository.getSuiteNr() > 0){
                    Repository.frame.mainpanel.p1.sc.g.updateLocations(Repository.getSuita(0));}
                Repository.frame.mainpanel.p1.sc.g.repaint();}});
        filemenu.add(changeuser);
        JMenuItem saveuser = new JMenuItem("Save suite file");
        saveuser.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                if(!sc.g.getUser().equals("")){
                    if(sc.g.printXML(sc.g.getUser(), false,false)) JOptionPane.showMessageDialog(Repository.frame, "File successfully saved ");
                    else JOptionPane.showMessageDialog(Repository.frame, "Warning, file not saved.");}}});
        filemenu.add(saveuser);
        JMenuItem deleteuser = new JMenuItem("Delete suite file");
        deleteuser.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                int r = JOptionPane.showConfirmDialog(null, "Delete file "+new File(sc.g.getUser()).getName()+" ?", "Delete", 0);
                if(r == 0){
                    Repository.emptyRepository();
                    try{new File(sc.g.getUser()).delete();
                        try{Repository.c.cd(Repository.getRemoteUsersDirectory());
                            Repository.c.rm(new File(sc.g.getUser()).getName());}
                        catch(Exception e){
                            System.out.println("Could not delete "+new File(sc.g.getUser()).getName()+" from "+Repository.getRemoteUsersDirectory());
                            e.printStackTrace();}}
                    catch(Exception e){e.printStackTrace();}
                    File usersdirectory = new File(Repository.getUsersDirectory());
                    String users[] = new String[usersdirectory.list().length + 1];
                    System.arraycopy(usersdirectory.list(), 0, users, 0, usersdirectory.list().length);
                    users[users.length - 1] = "New File";
                    String user = (String)JOptionPane.showInputDialog(null, "Please enter file name", "File Name", 1, null, users, "File Name");
                    if(user!=null){
                        if(user.equals("New File")){
                            Repository.emptyRepository();
                            user = JOptionPane.showInputDialog(null, "Please enter file name", "File Name", -1).toUpperCase();
                            (new XMLBuilder(Repository.getSuite())).writeXMLFile((new StringBuilder()).append(Repository.getUsersDirectory()).append(System.getProperty("file.separator")).append(user).append(".xml").toString(),false);
                            Repository.frame.mainpanel.p1.sc.g.setUser((new StringBuilder()).append(Repository.getUsersDirectory()).append(System.getProperty("file.separator")).append(user).append(".xml").toString());}
                        else if(user != null){
                            Repository.frame.mainpanel.p1.sc.g.setUser((new StringBuilder()).append(Repository.getUsersDirectory()).append(System.getProperty("file.separator")).append(user).toString());
                            Repository.frame.mainpanel.p1.sc.g.parseXML(new File((new StringBuilder()).append(Repository.getUsersDirectory()).append(System.getProperty("file.separator")).append(user).toString()));}}
                    else Repository.frame.mainpanel.p1.sc.g.setUser("");
                    if(Repository.getSuiteNr() > 0)Repository.frame.mainpanel.p1.sc.g.updateLocations(Repository.getSuita(0));
                    Repository.frame.mainpanel.p1.sc.g.repaint();
                    Repository.frame.mainpanel.p1.sc.g.repaint();}}});
        filemenu.add(deleteuser);
        JMenuItem openlocalXML = new JMenuItem("Open from local");
        openlocalXML.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                JFileChooser chooser = new JFileChooser(); 
                chooser.setFileFilter(new XMLFilter());
                chooser.setCurrentDirectory(new java.io.File("."));
                chooser.setDialogTitle("Select XML File"); 
                if (chooser.showOpenDialog(Repository.frame) == JFileChooser.APPROVE_OPTION) {                    
                    Repository.emptyRepository();
                    sc.g.setUser(Repository.getUsersDirectory()+Repository.getBar()+chooser.getSelectedFile().getName());
                    sc.g.parseXML(chooser.getSelectedFile());
                    if(Repository.getSuiteNr() > 0)sc.g.updateLocations(Repository.getSuita(0));
                    sc.g.repaint();}}});
        filemenu.add(openlocalXML);
        JMenuItem savelocalXML = new JMenuItem("Save to local");
        savelocalXML.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                if(!sc.g.getUser().equals("")){
                    try{JFileChooser chooser = new JFileChooser(); 
                        chooser.setApproveButtonText("Save");
                        chooser.setCurrentDirectory(new java.io.File("."));
                        chooser.setDialogTitle("Choose Location");         
                        chooser.setAcceptAllFileFilterUsed(false);    
                        if (chooser.showOpenDialog(Panel1.this) == JFileChooser.APPROVE_OPTION) {
                            if(sc.g.printXML(chooser.getSelectedFile()+".xml", false,true)) JOptionPane.showMessageDialog(Repository.frame, "File successfully saved ");
                            else JOptionPane.showMessageDialog(Repository.frame, "Warning, file not saved.");}
                        else {System.out.println("No Selection");}}
                    catch(Exception e){
                        JOptionPane.showMessageDialog(Repository.frame, "Warning, file not saved.");
                        System.out.println("There was a problem in writing xml file, make sure file it is not in use.");
                        e.printStackTrace();}}}});
        filemenu.add(savelocalXML);
        menu.add(filemenu);
        add(menu);
        tdtl = new TreeDropTargetListener(applet);        
        sc = new ScrollGrafic(10, 32, tdtl, user, applet);
        ep = new ExplorerPanel(470, 32, tdtl, applet, Repository.c);
        setLayout(null);    
        JSplitPane splitPane2 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,new JScrollPane(ep.tree),new TCDetails());
        splitPane2.setDividerLocation(0.5);        
        JSplitPane splitPane3 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,sc.pane,suitaDetails);
        splitPane3.setDividerLocation(0.5);        
        splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT,splitPane3,splitPane2);
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        splitPane.setBounds(10,45,(int)screenSize.getWidth()-80,600);
        splitPane.setDividerLocation(0.5);
        add(splitPane);
//         System.out.println("Finished Panel1 initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Finished Suites interface initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();}
    
    public void setOpenedfile(String filename){
        openedfile.setText("Suite file: "+filename);}}
        
class TreeDropTargetListener implements DropTargetListener {
    boolean applet;
    public TreeDropTargetListener(boolean applet){this.applet = applet;}
    public void dragEnter(DropTargetDragEvent dropTargetDragEvent){}
    public void dragExit(DropTargetEvent dropTargetEvent){}
    public void dragOver(DropTargetDragEvent dropTargetDragEvent) {
        Repository.frame.mainpanel.p1.sc.g.handleDraggingLine((int)dropTargetDragEvent.getLocation().getX(),(int)dropTargetDragEvent.getLocation().getY());}
    public void dropActionChanged(DropTargetDragEvent dropTargetDragEvent) {}
    public synchronized void drop(DropTargetDropEvent dropTargetDropEvent) {
        try{Repository.frame.mainpanel.p1.sc.g.clearDraggingLine();
            Repository.frame.mainpanel.p1.sc.g.drop((int)dropTargetDropEvent.getLocation().getX(),(int)dropTargetDropEvent.getLocation().getY());}
            catch(Exception e){e.printStackTrace();
                System.out.println("Could not get folder location");}}}