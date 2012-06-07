import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.event.MenuListener;
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
import javax.swing.event.MenuEvent;
import javax.swing.MenuSelectionManager;
import java.util.ArrayList;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.awt.FontMetrics;
import java.awt.Font;
import javax.swing.JTextField;
import javax.swing.ImageIcon;
import javax.swing.ToolTipManager;
import javax.swing.JComboBox;

/*
 * Suites generation panel
 */
public class Panel1 extends JPanel{
    private static final long serialVersionUID = 1L;
    public ScrollGrafic sc;
    public ExplorerPanel ep;//remote tc structure    
    private TreeDropTargetListener tdtl;
    private boolean applet;//if started from applet
    public JSplitPane splitPane;//split panel for suites and remote tc structure    
    public SuitaDetails suitaDetails;//details defined by user
    private JLabel openedfile;
    public JButton remove;
    private JButton generate;
    
    public Panel1(String user, final boolean applet, int width){
        Repository.intro.setStatus("Started Suites interface initialization");
        Repository.intro.addPercent(0.035);
        Repository.intro.repaint();
        openedfile = new JLabel();
        openedfile.setBounds(210,23,250,20);
        add(openedfile);
        JButton addsuite = new JButton(new ImageIcon(Repository.addsuitaicon));
        addsuite.setToolTipText("Add Suite");
        ToolTipManager.sharedInstance().setInitialDelay(400);
        addsuite.setBounds(10,20,40,25);
        add(addsuite);
        addsuite.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.addSuiteFromButton();}});        
        remove = new JButton(new ImageIcon(Repository.removeicon));
        remove.setToolTipText("Remove");
        remove.setBounds(52,20,40,25);
        remove.setEnabled(false);
        add(remove);
        remove.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.removeSelected();}});
        generate = new JButton("Generate");
        generate.setBounds(94,20,90,25);
        generate.setToolTipText("Generate XML");
        add(generate);
        suitaDetails = new SuitaDetails(Repository.getDatabaseUserFields());
        generate.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String result="";
                try{result = (String)Repository.getRPCClient().execute("getExecStatusAll",new Object[]{});}
                catch(Exception e){System.out.println("Could not connect to server");}
                int defsNr = suitaDetails.getDefsNr();
                boolean execute=true;
                for(int i=0;i<Repository.getSuiteNr();i++){
                    if(Repository.getSuita(i).getUserDefNr()<defsNr){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window, "Warning","Please set user defined fields for: "+Repository.getSuita(i).getName());
                        
//                         JOptionPane.showMessageDialog(Repository.window, "Please set user defined fields for: "+Repository.getSuita(i).getName());
                        execute = false;
                        break;}
                    for(int j=0;j<defsNr;j++){
                        if(Repository.getSuita(i).getUserDef(j)[1].length()==0&&Repository.getDatabaseUserFields().get(j)[Repository.MANDATORY].equals("true")){
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window, "Warning","Please set user defined field at "+Repository.getDatabaseUserFields().get(j)[Repository.LABEL]+" for: "+Repository.getSuita(i).getName());
//                             JOptionPane.showMessageDialog(Repository.window, "Please set user defined field at "+Repository.getDatabaseUserFields().get(j)[Repository.LABEL]+" for: "+Repository.getSuita(i).getName());
                            execute = false;
                            break;}}
                    if(!execute)break;}                
                if(execute){
                    if(!result.equals("running")){
                        sc.g.printXML(Repository.getTestXMLDirectory(),true,false);
                        Repository.emptyTestRepository();
                        File xml = new File(Repository.getTestXMLDirectory());    
                        int size = Repository.getLogs().size();
                        for(int i=5;i<size;i++){Repository.getLogs().remove(5);}
                        new XMLReader(xml).parseXML(sc.g.getGraphics(), true);
                        Repository.window.mainpanel.p2.updateTabs();
                        CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, Repository.window, "Info", "File successfully generated ");
//                         JOptionPane.showMessageDialog(Repository.window, "File successfully generated ");
                    }
                    else{
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window, "Warning", "Please close Central Engine before generating");
//                         JOptionPane.showMessageDialog(Repository.window, "Please close Central Engine before generating");
                    }}}});
        this.applet = applet;
        JMenuBar menu = new JMenuBar();
        menu.setLayout(null);
        menu.setBounds(0, 0, width, 20);
        
        final JMenu suitemenu = new JMenu("Suite");
        suitemenu.setBounds(50,0,50,20);
        menu.add(suitemenu);
        JMenuItem item ;
        item = new JMenuItem("Add Suite");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                System.out.println("adding suite");
                sc.g.addSuiteFromButton();}});
        suitemenu.add(item);
        item = new JMenuItem("Set Ep");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                /*
                 * get EP's from EP's file
                 */
                try{final Item theone = getItem();
                    File f = new File(Repository.temp+System.getProperty("file.separator")+"Twister"+System.getProperty("file.separator")+"EpID.txt");
                    String line = null;  
                    InputStream in = Repository.c.get(Repository.REMOTEEPIDDIR);
                    InputStreamReader inputStreamReader = new InputStreamReader(in);
                    BufferedReader bufferedReader = new BufferedReader(inputStreamReader);  
                    StringBuffer b=new StringBuffer("");
                    while ((line=bufferedReader.readLine())!= null){b.append(line+";");}                        
                    bufferedReader.close();
                    inputStreamReader.close();
                    in.close();
                    String result = b.toString();
                    String  [] vecresult = result.split(";");//EP's list
                    try{
                        JComboBox combo = new JComboBox(vecresult);
                        int resp = (Integer)CustomDialog.showDialog(combo,JOptionPane.INFORMATION_MESSAGE,JOptionPane.OK_CANCEL_OPTION,sc.g,"Please select an Ep name",null);
                        if(resp==JOptionPane.OK_OPTION){
                            String ID = combo.getSelectedItem().toString();
//                         String ID = (String)JOptionPane.showInputDialog(sc.g,"Please select an Ep name","EpID's", JOptionPane.INFORMATION_MESSAGE,null, vecresult,"EpID's");
                            theone.setEpId(ID);
                            for(int i=0;i<theone.getSubItemsNr();i++){
                                sc.g.assignEpID(theone.getSubItem(i),ID);}
                            repaint();}}
                    catch(Exception e){e.printStackTrace();}}
                catch(Exception e){e.printStackTrace();}}});
        item = new JMenuItem("Rename");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                final Item theone = getItem();
//                 String name = JOptionPane.showInputDialog(sc.g,"Please enter the suite name","Suite Name",  JOptionPane.PLAIN_MESSAGE).toUpperCase();
                String name = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION, sc.g, "Suite Name", "Please enter the suite name").toUpperCase();
                if(!name.equals("NULL")){
                    FontMetrics metrics = sc.g.getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 14));
                    int width = metrics.stringWidth(name)+140;
                    theone.setName(name);
                    theone.getRectangle().setSize(width,(int)theone.getRectangle().getHeight());
                    if(theone.isVisible())sc.g.updateLocations(theone);
                    sc.g.repaint();}}});
        item = new JMenuItem("Expand");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                final Item theone = getItem();
                theone.setVisible(true);
                sc.g.updateLocations(theone);
                sc.g.repaint();}});
        item = new JMenuItem("Contract");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                final Item theone = getItem();
                int nr = theone.getSubItemsNr();
                for(int i=0;i<nr;i++){
                    theone.getSubItem(i).setVisible(false);}
                sc.g.updateLocations(theone);
                repaint();}});
        item = new JMenuItem("Remove");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(sc.g.getSelectedCollection().size()>1){
                    sc.g.removeSelected();}
                else{final Item theone = getItem();
                    if(theone.getPos().size()==1){
                        int index = theone.getPos().get(0).intValue();
                        Repository.getSuite().remove(theone);                    
                        if(Repository.getSuiteNr()>=index){
                            for(int i= index;i<Repository.getSuiteNr();i++){
                                Repository.getSuita(i).updatePos(0,new Integer(Repository.getSuita(i).getPos().get(0).intValue()-1));}
                        if(Repository.getSuiteNr()>0){
                            Repository.getSuita(0).setLocation(new int[]{5,10});
                            sc.g.updateLocations(Repository.getSuita(0));}
                        sc.g.repaint();
                        sc.g.getSelectedCollection().clear();}}
                    else{int index = theone.getPos().get(theone.getPos().size()-1).intValue();
                        int position = theone.getPos().size()-1;
                        ArrayList<Integer> temp = (ArrayList<Integer>)theone.getPos().clone();
                        temp.remove(temp.size()-1);
                        Item parent = sc.g.getItem(temp,false);
                        parent.getSubItems().remove(theone);                    
                        if(parent.getSubItemsNr()>=index){
                            for(int i = index;i<parent.getSubItemsNr();i++){
                                parent.getSubItem(i).updatePos(position,new Integer(parent.getSubItem(i).getPos().get(position).intValue()-1));}}
                        sc.g.updateLocations(parent);
                        sc.g.repaint();
                        sc.g.getSelectedCollection().clear();}
                    for(int j=0;j<suitemenu.getMenuComponentCount();j++){
                        suitemenu.getMenuComponent(j).setEnabled(false);}}}});
        /*
         * set menu options
         * based on selection
         */
        suitemenu.addMenuListener(new MenuListener(){
            public void menuCanceled(MenuEvent ev){}
            public void menuDeselected(MenuEvent ev){}
            public void menuSelected(MenuEvent ev){
                for(int j=0;j<suitemenu.getMenuComponentCount();j++){
                    suitemenu.getMenuComponent(j).setEnabled(false);}
                if(sc.g.getSelectedCollection().size()>1){
                    suitemenu.getMenuComponent(5).setEnabled(true);}
                else{
                    if(sc.g.getSelectedCollection().size()==0){
                        suitemenu.getMenuComponent(0).setEnabled(true);}
                    if(sc.g.getSelectedCollection().size()==1){
                        ArrayList<Integer> temp = new ArrayList<Integer>();
                        int indexsize = sc.g.getSelectedCollection().get(0).length;
                        for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
                        final Item theone = sc.g.getItem(temp,false);
                        if(theone.getType()==2){
                            for(int j=0;j<suitemenu.getMenuComponentCount();j++){
                                suitemenu.getMenuComponent(j).setEnabled(true);}
                            if(theone.getPos().size()>1){
                                suitemenu.getMenuComponent(1).setEnabled(false);}}}}}});
                                
        final JMenu tcmenu = new JMenu("TestCase");
        tcmenu.setBounds(100,0,65,20);
        menu.add(tcmenu);
        
        item = new JMenuItem("Set Parameters");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                ArrayList<Integer> temp = new ArrayList<Integer>();
                int indexsize = sc.g.getSelectedCollection().get(0).length;
                for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
                sc.g.setParam(sc.g.getItem(temp,false));}});
        item = new JMenuItem("Add Property");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                ArrayList<Integer> temp = new ArrayList<Integer>();
                int indexsize = sc.g.getSelectedCollection().get(0).length;
                for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
                sc.g.addTCProp(sc.g.getItem(temp,false));}});
        item = new JMenuItem("Rename");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                final Item theone = getItem();
                
                
//                 String name = JOptionPane.showInputDialog(sc.g,"Please enter the TC name","TC Name",  JOptionPane.PLAIN_MESSAGE);
                
                String name = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION, sc.g, "TC Name", "Please enter the TC name").toUpperCase();
                if(!name.equals("NULL")){
                    FontMetrics metrics = sc.g.getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 13));
                    int width = metrics.stringWidth(name);
                    theone.setName(name);
                    theone.getRectangle().setSize(width+50,(int)theone.getRectangle().getHeight());
                    sc.g.updateLocations(theone);
                    sc.g.repaint();}}});
        item = new JMenuItem("Expand");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                final Item theone = getItem();
                theone.setVisible(true);
                sc.g.updateLocations(theone);
                sc.g.repaint();}});
        item = new JMenuItem("Contract");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                final Item theone = getItem();
                theone.setVisible(false);
                sc.g.updateLocations(theone);
                sc.g.repaint();}});
        item = new JMenuItem("Switch Runnable");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.switchRunnable();}});
        item = new JMenuItem("Set pre-requisites");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                ArrayList<Integer> temp = new ArrayList<Integer>();
                int indexsize = sc.g.getSelectedCollection().get(0).length;
                for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
                Item theone = sc.g.getItem(temp,false);
                sc.g.setPreRequisites(theone);}});
        item = new JMenuItem("Unset pre-requisites");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                ArrayList<Integer> temp = new ArrayList<Integer>();
                int indexsize = sc.g.getSelectedCollection().get(0).length;
                for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
                Item theone = sc.g.getItem(temp,false);
                theone.setPrerequisite(false);
                sc.g.repaint();}});
        item = new JMenuItem("Remove");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(sc.g.getSelectedCollection().size()>1){
                    sc.g.removeSelected();}
                else{
                    ArrayList<Integer> temp = new ArrayList<Integer>();
                    int indexsize = sc.g.getSelectedCollection().get(0).length;
                    for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
                    final Item theone = sc.g.getItem(temp,false);
                    sc.g.removeTC(theone);
                    sc.g.getSelectedCollection().clear();}}});
        /*
         * set menu options
         * based on selection
         */
        tcmenu.addMenuListener(new MenuListener(){
            public void menuCanceled(MenuEvent ev){}
            public void menuDeselected(MenuEvent ev){}
            public void menuSelected(MenuEvent ev){
                for(int j=0;j<tcmenu.getMenuComponentCount();j++){
                    tcmenu.getMenuComponent(j).setEnabled(false);}
                if(sc.g.getSelectedCollection().size()>1){
                    tcmenu.getMenuComponent(5).setEnabled(true);}
                else{
                    if(sc.g.getSelectedCollection().size()==1){
                        ArrayList<Integer> temp = new ArrayList<Integer>();
                        int indexsize = sc.g.getSelectedCollection().get(0).length;
                        for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
                        final Item theone = sc.g.getItem(temp,false);
                        if(theone.getType()==1){
                            for(int j=0;j<tcmenu.getMenuComponentCount();j++){
                                tcmenu.getMenuComponent(j).setEnabled(true);}
                            if(!theone.isPrerequisite()){
                                tcmenu.getMenuComponent(7).setEnabled(false);}
                            else tcmenu.getMenuComponent(6).setEnabled(false);}}}}});
                                
        JMenu filemenu = new JMenu("File");
        filemenu.setBounds(10,0,40,20);
        JMenuItem newuser = new JMenuItem("New suite file");
        newuser.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
//                 String user ="";
//                 Repository.emptySuites();
//                 try{user = JOptionPane.showInputDialog(null, "Please enter file name", "File Name", -1).toUpperCase();}
//                 catch(NullPointerException e){}
                String user = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION, sc.g, "TC Name", "Please enter the TC name").toUpperCase();
                if(user!=null){
                    (new XMLBuilder(Repository.getSuite())).writeXMLFile(Repository.getUsersDirectory()+System.getProperty("file.separator")+user+".xml",false);
                    Repository.window.mainpanel.p1.sc.g.setUser(Repository.getUsersDirectory()+System.getProperty("file.separator")+user+".xml");
                    sc.g.printXML(sc.g.getUser(),false,false);
                    sc.g.updateScroll();
                    sc.g.repaint();
                    Repository.emptySuites();}}});
        filemenu.add(newuser);
        JMenuItem changeuser = new JMenuItem("Open suite file");
        changeuser.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                File usersdirectory = new File(Repository.getUsersDirectory());
                String users[] = new String[usersdirectory.list().length];
                System.arraycopy(usersdirectory.list(), 0, users, 0, usersdirectory.list().length);
//                 String user = (String)JOptionPane.showInputDialog(null, "Select suite file", "Suite File", 1, null, users, "Suite File");
                JComboBox combo = new JComboBox(users);
                int resp = (Integer)CustomDialog.showDialog(combo,JOptionPane.INFORMATION_MESSAGE,JOptionPane.OK_CANCEL_OPTION,sc.g,"Select suite file",null);
                if(resp==JOptionPane.OK_OPTION){
                    String user = combo.getSelectedItem().toString();
//                 if(user != null){
                    Repository.emptySuites();
                    Repository.window.mainpanel.p1.sc.g.setUser(Repository.getUsersDirectory()+Repository.getBar()+user);
                    System.out.println("TEST: "+Repository.getUsersDirectory()+Repository.getBar()+user);
                    Repository.window.mainpanel.p1.sc.g.parseXML(new File(Repository.getUsersDirectory()+Repository.getBar()+user));}
                if(Repository.getSuiteNr() > 0){
                    Repository.window.mainpanel.p1.sc.g.updateLocations(Repository.getSuita(0));}
                Repository.window.mainpanel.p1.sc.g.repaint();}});
        filemenu.add(changeuser);
        JMenuItem saveuser = new JMenuItem("Save suite file");
        saveuser.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                if(!sc.g.getUser().equals("")){
                    if(sc.g.printXML(sc.g.getUser(), false,false))CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, Repository.window, "Succes", "File successfully saved");
//                     JOptionPane.showMessageDialog(Repository.window, "File successfully saved");
                    else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window, "Warning", "Warning, file not saved");}}});
//                     JOptionPane.showMessageDialog(Repository.window, "Warning, file not saved.");
        filemenu.add(saveuser);
        JMenuItem deleteuser = new JMenuItem("Delete suite file");
        deleteuser.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                int r = (Integer)CustomDialog.showDialog(new JLabel( "Delete file "+new File(sc.g.getUser()).getName()+" ?"), JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION, sc.g, "Delete", null);
//                 int r = JOptionPane.showConfirmDialog(null, "Delete file "+new File(sc.g.getUser()).getName()+" ?", "Delete", 0);
                if(r == JOptionPane.OK_OPTION){
                    Repository.emptySuites();
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
                    JComboBox combo = new JComboBox(users);
//                     String user = (String)JOptionPane.showInputDialog(null, "Please select file name", "File Name", 1, null, users, "File Name");
//                     if(user!=null){
                    int resp = (Integer)CustomDialog.showDialog(combo,JOptionPane.INFORMATION_MESSAGE,JOptionPane.OK_CANCEL_OPTION,Panel1.this,"File Name",null);
                    if(resp==JOptionPane.OK_OPTION){
                        String user = combo.getSelectedItem().toString();
                        if(user.equals("New File")){
                            
//                             user = JOptionPane.showInputDialog(null, "Please enter file name", "File Name", -1).toUpperCase();
                            user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION, Panel1.this, "File Name", "Please enter file name").toUpperCase();
                            if(!user.equals("NULL")){
                                Repository.emptySuites();
                                (new XMLBuilder(Repository.getSuite())).writeXMLFile((new StringBuilder()).append(Repository.getUsersDirectory()).append(System.getProperty("file.separator")).append(user).append(".xml").toString(),false);
                                sc.g.setUser((new StringBuilder()).append(Repository.getUsersDirectory()).append(System.getProperty("file.separator")).append(user).append(".xml").toString());
                                sc.g.printXML(sc.g.getUser(),false,false);}}
                        else if(user != null){
                            sc.g.setUser((new StringBuilder()).append(Repository.getUsersDirectory()).append(System.getProperty("file.separator")).append(user).toString());
                            sc.g.parseXML(new File((new StringBuilder()).append(Repository.getUsersDirectory()).append(System.getProperty("file.separator")).append(user).toString()));}}
                    else Repository.window.mainpanel.p1.sc.g.setUser("");
                    if(Repository.getSuiteNr() > 0)Repository.window.mainpanel.p1.sc.g.updateLocations(Repository.getSuita(0));
                    Repository.window.mainpanel.p1.sc.g.repaint();
                    Repository.window.mainpanel.p1.sc.g.repaint();}}});
        filemenu.add(deleteuser);
        JMenuItem openlocalXML = new JMenuItem("Open from local");
        openlocalXML.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                JFileChooser chooser = new JFileChooser(); 
                chooser.setFileFilter(new XMLFilter());
                chooser.setCurrentDirectory(new java.io.File("."));
                chooser.setDialogTitle("Select XML File"); 
                if (chooser.showOpenDialog(Repository.window) == JFileChooser.APPROVE_OPTION) {                    
                    Repository.emptySuites();
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
                            if(sc.g.printXML(chooser.getSelectedFile()+".xml", false,true)) CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, Panel1.this, "Success","File successfully saved ");
//                             JOptionPane.showMessageDialog(Repository.window, "File successfully saved ");
                            else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Panel1.this, "Warning","Warning, file not saved.");}
//                             JOptionPane.showMessageDialog(Repository.window, "Warning, file not saved.");}
                        else {System.out.println("No Selection");}}
                    catch(Exception e){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Panel1.this, "Warning","Warning, file not saved.");
//                         JOptionPane.showMessageDialog(Repository.window, "Warning, file not saved.");
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
        Repository.intro.setStatus("Finished Suites interface initialization");
        Repository.intro.addPercent(0.035);
        Repository.intro.repaint();}
        
    public Item getItem(){
        ArrayList<Integer> temp = new ArrayList<Integer>();
        int indexsize = sc.g.getSelectedCollection().get(0).length;
        for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
        return sc.g.getItem(temp,false);}
        
    /*
     * generate button status
     * based on CE status
     */
    public void setGenerate(boolean status){
        if(!status){
            if(generate.isEnabled()){
                generate.setEnabled(status);
                generate.setToolTipText("stop CE to enable");}}
        else{
            if(!generate.isEnabled()){
                generate.setEnabled(status);
                generate.setToolTipText("Generate XML");}}}
    
    public void setOpenedfile(String filename){
        openedfile.setText("Suite file: "+filename);}}
        
class TreeDropTargetListener implements DropTargetListener {
    boolean applet;
    public TreeDropTargetListener(boolean applet){this.applet = applet;}
    public void dragEnter(DropTargetDragEvent dropTargetDragEvent){}
    public void dragExit(DropTargetEvent dropTargetEvent){}
    public void dragOver(DropTargetDragEvent dropTargetDragEvent) {
        Repository.window.mainpanel.p1.sc.g.handleDraggingLine((int)dropTargetDragEvent.getLocation().getX(),(int)dropTargetDragEvent.getLocation().getY());}
    public void dropActionChanged(DropTargetDragEvent dropTargetDragEvent) {}
    public synchronized void drop(DropTargetDropEvent dropTargetDropEvent) {
        try{Repository.window.mainpanel.p1.sc.g.clearDraggingLine();
            Repository.window.mainpanel.p1.sc.g.drop((int)dropTargetDropEvent.getLocation().getX(),(int)dropTargetDropEvent.getLocation().getY());}
            catch(Exception e){e.printStackTrace();
                System.out.println("Could not get folder location");}}}