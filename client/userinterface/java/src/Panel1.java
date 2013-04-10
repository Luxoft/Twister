/*
File: Panel1.java ; This file is part of Twister.
Version: 2.001

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
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
import javax.swing.JCheckBox;
import com.twister.Item;
import java.awt.Cursor;
import java.awt.Component;
import javax.swing.JList;
import java.util.Arrays;
import javax.swing.SwingUtilities;
import java.io.BufferedWriter;
import java.io.FileWriter;
import com.twister.CustomDialog;
import java.util.HashMap;
import java.util.Set;
import java.util.Iterator;

/*
 * Suites generation panel
 */
public class Panel1 extends JPanel{
    private static final long serialVersionUID = 1L;
    public ScrollGrafic sc;
    public ExplorerPanel ep;//remote tc structure    
    private TreeDropTargetListener tdtl;
    private boolean applet;//if started from applet
    public JSplitPane splitPane,splitPane2,splitPane3;//split panel for suites and remote tc structure    
    public SuitaDetails suitaDetails;//details defined by user
    private JLabel openedfile;
    public JButton remove,generate,showoptionals,addsuite,edit;
    private TCDetails tcdetails = new TCDetails();
    
    public Panel1(String user, final boolean applet, int width){
        Repository.intro.setStatus("Started Suites interface initialization");
        Repository.intro.addPercent(0.035);
        Repository.intro.repaint();
        openedfile = new JLabel();
        openedfile.setBounds(410,22,250,20);
        add(openedfile);
        addsuite = new JButton(new ImageIcon(Repository.addsuitaicon));
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
        generate = new JButton("Run",new ImageIcon(Repository.getPlayIcon()));
        generate.setBounds(94,20,105,25);
        generate.setToolTipText("Run suite");
        add(generate);
        showoptionals = new JButton("Show optionals");
        showoptionals.setBounds(205,20,150,25);
        showoptionals.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                showOptionals();}});
        add(showoptionals);
        suitaDetails = new SuitaDetails(Repository.getDatabaseUserFields());
        generate.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                generate();}});
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
                sc.g.addSuiteFromButton();}});
        suitemenu.add(item);
        item = new JMenuItem("Set TB");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                 setEP();
            }});
        item = new JMenuItem("Rename");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                renameSuite();}});
        item = new JMenuItem("Expand");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                expandContract(true);}});
        item = new JMenuItem("Contract");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                contractSuite();}});
        item = new JMenuItem("Remove");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeSuite(suitemenu);}});
        suitemenu.addMenuListener(new MenuListener(){
            public void menuCanceled(MenuEvent ev){}
            public void menuDeselected(MenuEvent ev){}
            public void menuSelected(MenuEvent ev){
                enableSuiteMenu(suitemenu);}});
        final JMenu tcmenu = new JMenu("TestCase");
        tcmenu.setBounds(100,0,75,20);
        menu.add(tcmenu);
        item = new JMenuItem("Set Parameters");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setParam();}});
        item = new JMenuItem("Add Property");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addTCProperty();}});
        item = new JMenuItem("Rename");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                renameTC();}});
        item = new JMenuItem("Expand");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                expandContract(true);}});
        item = new JMenuItem("Contract");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                expandContract(false);}});
        item = new JMenuItem("Switch Runnable");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.switchRunnable();}});
        item = new JMenuItem("Set pre-requisites");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                setPrerequisite();}});
        item = new JMenuItem("Unset pre-requisites");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                unsetPrerequisite();}});
        item = new JMenuItem("Remove");
        tcmenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeElement();}});
        tcmenu.addMenuListener(new MenuListener(){
            public void menuCanceled(MenuEvent ev){}
            public void menuDeselected(MenuEvent ev){}
            public void menuSelected(MenuEvent ev){
                enableTCMenu(tcmenu);}});
        JMenu filemenu = new JMenu("File");
        filemenu.setBounds(10,0,40,20);
        JMenuItem newuser = new JMenuItem("New project file");
        newuser.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addSuiteFile();}});
        filemenu.add(newuser);
        JMenuItem changeuser = new JMenuItem("Open project file");
        changeuser.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Repository.openProjectFile();
            }});
        filemenu.add(changeuser);
        JMenuItem saveuser = new JMenuItem("Save project file");
        saveuser.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveSuiteFile();}});
        filemenu.add(saveuser);
        
        JMenuItem saveuseras = new JMenuItem("Save project as");
        saveuseras.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveSuiteAs();}});
        filemenu.add(saveuseras);
        
        JMenuItem deleteuser = new JMenuItem("Delete project file");
        deleteuser.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                deleteSuiteFile();}});
        filemenu.add(deleteuser);
        JMenuItem openlocalXML = new JMenuItem("Open from local");
        openlocalXML.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                openLocalFile();}});
        filemenu.add(openlocalXML);
        JMenuItem savelocalXML = new JMenuItem("Save to local");
        savelocalXML.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveLocalXML();}});
        filemenu.add(savelocalXML);
        menu.add(filemenu);
        add(menu);
        tdtl = new TreeDropTargetListener(applet);        
        sc = new ScrollGrafic(10, 32, tdtl, user, applet);
        ep = new ExplorerPanel(470, 32, tdtl, applet);
        //ep = new ExplorerPanel(470, 32, tdtl, applet, Repository.c);
        setLayout(null);    
        splitPane2 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                                                new JScrollPane(ep.tree),
                                                tcdetails);
        try{
            SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    splitPane2.setDividerLocation(Repository.getLayouts().
                                                 get("mainh2splitlocation").getAsInt());
                }
            });
        } catch(Exception e){
            splitPane2.setDividerLocation(0.5);
        }           
        splitPane3 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                                                sc.pane,suitaDetails);
        try{
            SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    splitPane3.setDividerLocation(Repository.getLayouts().
                                                 get("mainh1splitlocation").getAsInt());
                }
            });
        } catch(Exception e){
            splitPane3.setDividerLocation(0.5);
        }       
        splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT,
                                    splitPane3,splitPane2);
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        splitPane.setBounds(10,45,(int)screenSize.getWidth()-80,600);
        
        try{
            SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    splitPane.setDividerLocation(Repository.getLayouts().
                                                 get("mainvsplitlocation").getAsInt());
                }
            });
        } catch(Exception e){
            splitPane.setDividerLocation(0.5);
        }
        add(splitPane);
        Repository.intro.setStatus("Finished Suites interface initialization");
        Repository.intro.addPercent(0.035);
        Repository.intro.repaint();
        edit = new JButton("Edit");
        edit.setBounds(10,20,65,25);
        edit.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                edit();}});}
        
        
    /*
     * method to show optionals tc
     * in suites tab
     */
    public void showOptionals(){
        boolean show;
        if(Repository.getSuiteNr()>0){
            if(showoptionals.getText().equals("Show optionals")){
                showoptionals.setText("Show all");
                sc.g.setOnlyOptionals(true);
                sc.g.showOptionals(null);
                sc.g.updateLocations(Repository.getSuita(0));
                sc.g.repaint();
                return;
            }
            showoptionals.setText("Show optionals");
                sc.g.setOnlyOptionals(false);
                sc.g.showOptionals(null);
                sc.g.updateLocations(Repository.getSuita(0));
                sc.g.repaint();
                return;
    }}
    
    
    /*
     * save opened suite file
     * on server with name provided by user
     */
    private void saveSuiteAs(){
        if(!sc.g.getUser().equals("")){
            String user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, Repository.window,
                                                    "File Name", "Please enter project file name").
                                                    toUpperCase();
            
            if(user!=null&&!user.equals("")){
                if(sc.g.printXML(user+".xml", false,false,
                             Repository.window.mainpanel.p1.suitaDetails.stopOnFail(),
                             Repository.window.mainpanel.p1.suitaDetails.saveDB(),
                             Repository.window.mainpanel.p1.suitaDetails.getDelay()))
                    CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, 
                                            Repository.window, "Succes",
                                            "File successfully saved");
                else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                            Repository.window, "Warning", 
                                            "Warning, file not saved");}}}
        
    /*
     * save opened suite file
     * on server
     */
    private void saveSuiteFile(){
        if(!sc.g.getUser().equals("")){
            if(sc.g.printXML(sc.g.getUser(), false,false,
                             Repository.window.mainpanel.p1.suitaDetails.stopOnFail(),
                             Repository.window.mainpanel.p1.suitaDetails.saveDB(),
                             Repository.window.mainpanel.p1.suitaDetails.getDelay()
                             ))
                CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, 
                                        Repository.window, "Succes",
                                        "File successfully saved");
            else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                        Repository.window, "Warning", 
                                        "Warning, file not saved");}}
        
    /*
     * contract selected suite
     */
    private void contractSuite(){
        final Item theone = getItem();
        int nr = theone.getSubItemsNr();
        for(int i=0;i<nr;i++){
            theone.getSubItem(i).setVisible(false);}
        sc.g.updateLocations(theone);
        repaint();}
        
    /*
     * remove selected suite
     */
    private void removeSuite(JMenu suitemenu){
        if(sc.g.getSelectedCollection().size()>1){
            sc.g.removeSelected();}
        else{final Item theone = getItem();
            if(theone.getPos().size()==1){
                int index = theone.getPos().get(0).intValue();
                Repository.getSuite().remove(theone);                    
                if(Repository.getSuiteNr()>=index){
                    for(int i= index;i<Repository.getSuiteNr();i++){
                        Repository.getSuita(i).updatePos(0,
                                    new Integer(Repository.getSuita(i).
                                    getPos().get(0).intValue()-1));}
                if(Repository.getSuiteNr()>0){
                    Repository.getSuita(0).setLocation(new int[]{5,10});
                    sc.g.updateLocations(Repository.getSuita(0));}
                sc.g.repaint();
                sc.g.getSelectedCollection().clear();}}
            else{
                int index = theone.getPos().get(theone.getPos().
                                            size()-1).intValue();
                int position = theone.getPos().size()-1;
                ArrayList<Integer> temp = (ArrayList<Integer>)theone.getPos().clone();
                temp.remove(temp.size()-1);
                Item parent = sc.g.getItem(temp,false);
                parent.getSubItems().remove(theone);                    
                if(parent.getSubItemsNr()>=index){
                    for(int i = index;i<parent.getSubItemsNr();i++){
                        parent.getSubItem(i).updatePos(position,
                                                        new Integer(parent.getSubItem(i).
                                                        getPos().get(position).
                                                            intValue()-1));}}
                sc.g.updateLocations(parent);
                sc.g.repaint();
                sc.g.getSelectedCollection().clear();}
            for(int j=0;j<suitemenu.getMenuComponentCount();j++){
                suitemenu.getMenuComponent(j).setEnabled(false);}}}
        
    /*
     * set parameters for
     * selected TC
     */
    private void setParam(){        
        ArrayList<Integer> temp = new ArrayList<Integer>();
        int indexsize = sc.g.getSelectedCollection().get(0).length;
        for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
        sc.g.setParam(sc.g.getItem(temp,false));}
        
    /*
     * set menu options
     * based on selection
     */
    private void enableSuiteMenu(JMenu suitemenu){
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
                        suitemenu.getMenuComponent(1).setEnabled(false);}}}}}
        
    /*
     * add property to 
     * selected TC
     */    
    private void addTCProperty(){
        ArrayList<Integer> temp = new ArrayList<Integer>();
        int indexsize = sc.g.getSelectedCollection().get(0).length;
        for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
        sc.g.addTCProp(sc.g.getItem(temp,false));}
        
    /*
     * rename selected TC
     */
    private void renameTC(){
        final Item theone = getItem();
        String name = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
                                                    sc.g, "TC Name", "Please enter the TC name").toUpperCase();
        if(!name.equals("NULL")){
            FontMetrics metrics = sc.g.getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 13));
            int width = metrics.stringWidth(name);
            theone.setName(name);
            theone.getRectangle().setSize(width+50,(int)theone.getRectangle().getHeight());
            sc.g.updateLocations(theone);
            sc.g.repaint();}}
        
    /*
     * expand or contract
     * selected item
     */
    private void expandContract(boolean expand){
        final Item theone = getItem();
        theone.setVisible(expand);
        sc.g.updateLocations(theone);
        sc.g.repaint();}
        
    /*
     * rename selected suite
     */
    private void renameSuite(){
        final Item theone = getItem();
        String name = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION, sc.g,
                                                    "Suite Name", "Please enter the suite name").toUpperCase();
        if(!name.equals("NULL")){
            FontMetrics metrics = sc.g.getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 14));
            int width = metrics.stringWidth(name)+140;
            theone.setName(name);
            theone.getRectangle().setSize(width,(int)theone.getRectangle().getHeight());
            if(theone.isVisible())sc.g.updateLocations(theone);
            sc.g.repaint();}}
        
    /*
     * set Pre-requisite for selected item
     */
    private void setPrerequisite(){
        ArrayList<Integer> temp = new ArrayList<Integer>();
        int indexsize = sc.g.getSelectedCollection().get(0).length;
        for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
        Item theone = sc.g.getItem(temp,false);
        sc.g.setPreRequisites(theone);}
        
    /*
     * unset Pre-requisite for selected item
     */
    private void unsetPrerequisite(){
        ArrayList<Integer> temp = new ArrayList<Integer>();
        int indexsize = sc.g.getSelectedCollection().get(0).length;
        for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
        Item theone = sc.g.getItem(temp,false);
        theone.setPrerequisite(false);
        sc.g.repaint();}
        
    /*
     * remove selected element
     */
    private void removeElement(){
        if(sc.g.getSelectedCollection().size()>1){
            sc.g.removeSelected();}
        else{
            ArrayList<Integer> temp = new ArrayList<Integer>();
            int indexsize = sc.g.getSelectedCollection().get(0).length;
            for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
            final Item theone = sc.g.getItem(temp,false);
            sc.g.removeTC(theone);
            sc.g.getSelectedCollection().clear();}}
        
    /*
     * interpret selection and enable 
     * items based on selection
     */
    private void enableTCMenu(JMenu tcmenu){
        for(int j=0;j<tcmenu.getMenuComponentCount();j++){
            tcmenu.getMenuComponent(j).setEnabled(false);}
        if(sc.g.getSelectedCollection().size()>1){//if more tc's are selected
            tcmenu.getMenuComponent(5).setEnabled(true);}
        else{
            if(sc.g.getSelectedCollection().size()==1){//only one selected
                ArrayList<Integer> temp = new ArrayList<Integer>();
                int indexsize = sc.g.getSelectedCollection().get(0).length;
                for(int j=0;j<indexsize;j++){temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
                final Item theone = sc.g.getItem(temp,false);
                if(theone.getType()==1){
                    for(int j=0;j<tcmenu.getMenuComponentCount();j++){
                        tcmenu.getMenuComponent(j).setEnabled(true);}
                    if(!theone.isPrerequisite()){
                        tcmenu.getMenuComponent(7).setEnabled(false);}
                    else tcmenu.getMenuComponent(6).setEnabled(false);}}}}
                    
    public void edit(){
        splitPane3.setLeftComponent(sc.pane);
        try{
            SwingUtilities.invokeLater(new Runnable(){
                public void run() {
                    splitPane3.setDividerLocation(Repository.getLayouts().
                                                 get("mainh1splitlocation").getAsInt());
                }
            });
        } catch(Exception e){
            splitPane3.setDividerLocation(0.5);
        }   
        remove(edit);
        remove(Repository.window.mainpanel.getP2().play);
        remove(Repository.window.mainpanel.getP2().stop);        
        remove(Repository.window.mainpanel.getP2().cestatus); 
        add(openedfile);
        add(remove);
        add(generate);
        add(showoptionals);
        add(addsuite);
        suitaDetails.setEnabled(true);
        tcdetails.tcdetails.doClick();
        String user = "last_edited.xml";
        Repository.emptySuites();
        if(Repository.window.mainpanel.p1.sc.g.getUser()==null&&
           Repository.window.mainpanel.p1.sc.g.getUser().equals("")){
              Repository.window.mainpanel.p1.sc.g.setUser(Repository.getUsersDirectory()+
                                                            Repository.getBar()+user);
        }
        
        
        try{
            
            
            File file = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"Users"+Repository.getBar()+user);
            BufferedWriter writer = new BufferedWriter(new FileWriter(file));
            String content = Repository.getRemoteFileContent(Repository.getRemoteUsersDirectory()+"/"+user);
            writer.write(content);
            writer.close();
//             
//             InputStream in = Repository.c.get(Repository.getRemoteUsersDirectory()+"/"+user);
//             InputStreamReader inputStreamReader = new InputStreamReader(in);
//             BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
//             File file = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"Users"+Repository.getBar()+user);
//             BufferedWriter writer = new BufferedWriter(new FileWriter(file));
//             String line;
//             while ((line=bufferedReader.readLine())!= null){
//                 writer.write(line);
//                 writer.newLine();}
//             bufferedReader.close();
//             writer.close();
//             inputStreamReader.close();
//             in.close();
        } catch (Exception e){
            e.printStackTrace();
        }
        
        Repository.window.mainpanel.p1.sc.g.parseXML(new File(Repository.getUsersDirectory()+
                                                              Repository.getBar()+user));
        if(Repository.getSuiteNr() > 0){
            Repository.window.mainpanel.p1.sc.g.updateLocations(Repository.getSuita(0));}
        Repository.window.mainpanel.p1.suitaDetails.setGlobalDetails();
        Repository.window.mainpanel.p1.sc.g.repaint();
        repaint();
    }    
       
    /*
     * generate master suites XML
     */
    private void generate(){
        Repository.window.mainpanel.getP2().setSaveDB(suitaDetails.saveDB());
//         String result="";//server status
//         try{result = (String)Repository.getRPCClient().execute("getExecStatusAll",new Object[]{Repository.getUser()});}
//         catch(Exception e){
//             System.out.println("Could not connect to server");
//             e.printStackTrace();}
        int defsNr = suitaDetails.getDefsNr();
        boolean execute=true;
        for(int i=0;i<Repository.getSuiteNr();i++){
            /*
             * check if mandatory fields are set
             */
            for(int j=0;j<defsNr;j++){
                if( Repository.getDatabaseUserFields().get(j)[Repository.MANDATORY].equals("true") &&
                (Repository.getSuita(i).getUserDefNr()-1<j||Repository.getSuita(i).getUserDef(j)[1].length()==0)){
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window,
                                            "Warning","Please set user defined field at "+
                                            Repository.getDatabaseUserFields().get(j)[Repository.LABEL]+
                                            " for: "+Repository.getSuita(i).getName());
                    execute = false;
                    break;}}
        }
        
        Node parent = Repository.window.mainpanel.p4.getTB().getParentNode();
        boolean found ;
        for(Item i:Repository.getSuite()){
            for(String tb:i.getEpId()){
                Iterator iter = parent.getChildren().keySet().iterator();
                found = false;
                while(iter.hasNext()){
                    Node child = parent.getChild(iter.next().toString());
                    if(child!=null&&child.getName().equals(tb)){
                        if(child.getEPs()==null){
                            break;
                        }
                        if(!child.getEPs().equals("")){
                            found = true;
                        }
                        break;
                    }
                    if(found)break;
                }
                if(!found){
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Repository.window,
                                        "Warning","Please set EP for TB: "+ tb);
                    execute = false;
                    break;
                }
            }
        }
        
        
        
        
        if(execute){
            String [] s = sc.g.getUser().split("\\\\");
            if(s.length>0){
                s[s.length-1] = "last_edited.xml";
                StringBuilder st = new StringBuilder();
                for(String i:s){
                    st.append(i);
                    st.append("\\");
                }
                st.deleteCharAt(st.length()-1);
                String user = st.toString();
                if(sc.g.printXML(user, false,false,
                                 suitaDetails.stopOnFail(),
                                 suitaDetails.saveDB(),
                                 suitaDetails.getDelay())){}
                else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                            Repository.window, "Warning", 
                                            "Warning, temp file not saved");                    
            }
            sc.g.printXML(Repository.getTestXMLDirectory(),true,false,
                          suitaDetails.stopOnFail(),suitaDetails.saveDB(),
                          suitaDetails.getDelay());
            Repository.emptyTestRepository();
            File xml = new File(Repository.getTestXMLDirectory());
            int size = Repository.getLogs().size();
            for(int i=5;i<size;i++){Repository.getLogs().remove(5);}
            new XMLReader(xml).parseXML(sc.g.getGraphics(), true);
            setRunning();
        }
    }
    
    public void setRunning(){
        splitPane3.setLeftComponent(Repository.window.mainpanel.getP2().sc.pane);
        try{
            SwingUtilities.invokeLater(new Runnable(){
                public void run() {
                    splitPane3.setDividerLocation(Repository.getLayouts().
                                                 get("mainh1splitlocation").getAsInt());
                }
            });
        } catch(Exception e){
            splitPane3.setDividerLocation(0.5);
        }   
        remove(openedfile);
        remove(remove);
        remove(generate);
        remove(showoptionals);
        remove(addsuite);
        add(edit);
        add(Repository.window.mainpanel.getP2().play);
        add(Repository.window.mainpanel.getP2().stop);        
        add(Repository.window.mainpanel.getP2().cestatus);
        Repository.window.mainpanel.getP2().play.doClick();
        suitaDetails.setEnabled(false);
        tcdetails.logs.doClick();
        repaint();
    }
        
    /*
     * delete curently opened file
     * from local and server
     */
    private void deleteSuiteFile(){
        int r = (Integer)CustomDialog.showDialog(new JLabel( "Delete file "+
                                                            new File(sc.g.getUser()).getName()+" ?"),
                                                            JOptionPane.QUESTION_MESSAGE, 
                                                            JOptionPane.OK_CANCEL_OPTION, sc.g,
                                                            "Delete", null);
        if(r == JOptionPane.OK_OPTION){
            Repository.emptySuites();
            try{new File(sc.g.getUser()).delete();
                if(!Repository.removeRemoteFile(Repository.getRemoteUsersDirectory()+(new File(sc.g.getUser()).getName()))){
                    System.out.println("Could not delete "+new File(sc.g.getUser()).getName()+
                                        " from "+Repository.getRemoteUsersDirectory());
                }
//                 try{Repository.c.cd(Repository.getRemoteUsersDirectory());
//                     Repository.c.rm(new File(sc.g.getUser()).getName());}
//                 catch(Exception e){
//                     System.out.println("Could not delete "+new File(sc.g.getUser()).getName()+
//                                         " from "+Repository.getRemoteUsersDirectory());
//                     e.printStackTrace();}
            }
            catch(Exception e){e.printStackTrace();}
            File usersdirectory = new File(Repository.getUsersDirectory());
            String users[] = new String[usersdirectory.list().length + 1];
            System.arraycopy(usersdirectory.list(), 0, users, 0, usersdirectory.list().length);
            users[users.length - 1] = "New File";
            JComboBox combo = new JComboBox(users);
            int resp = (Integer)CustomDialog.showDialog(combo,JOptionPane.INFORMATION_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION,Panel1.this,
                                                        "File Name",null);
            if(resp==JOptionPane.OK_OPTION){
                String user = combo.getSelectedItem().toString();
                if(user.equals("New File")){
                    user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
                                                        Panel1.this, "File Name", "Please enter file name").toUpperCase();
                    if(!user.equals("NULL")){
                        Repository.emptySuites();
                        (new XMLBuilder(Repository.getSuite())).writeXMLFile((new StringBuilder()).
                                                               append(Repository.getUsersDirectory()).
                                                               append(System.getProperty("file.separator"))
                                                               .append(user).append(".xml").toString(),false,false);
                        sc.g.setUser((new StringBuilder()).append(Repository.getUsersDirectory()).
                                                                    append(System.getProperty("file.separator")).
                                                                    append(user).append(".xml").toString());
                        sc.g.printXML(sc.g.getUser(),false,false,false,false,"");}}
                else if(user != null){
                    sc.g.setUser((new StringBuilder()).append(Repository.getUsersDirectory()).
                                                                append(System.getProperty("file.separator")).
                                                                append(user).toString());
                    sc.g.parseXML(new File((new StringBuilder()).append(Repository.getUsersDirectory()).
                                                                append(System.getProperty("file.separator")).
                                                                append(user).toString()));}}
            else Repository.window.mainpanel.p1.sc.g.setUser("");
            if(Repository.getSuiteNr() > 0)Repository.window.mainpanel.p1.sc.g.updateLocations(Repository.getSuita(0));
            Repository.window.mainpanel.p1.sc.g.repaint();
            Repository.window.mainpanel.p1.sc.g.repaint();}}
        
    /*
     * open XML file from
     * local PC
     */    
    private void openLocalFile(){
        JFileChooser chooser = new JFileChooser(); 
        chooser.setFileFilter(new XMLFilter());
        chooser.setCurrentDirectory(new java.io.File("."));
        chooser.setDialogTitle("Select XML File"); 
        if (chooser.showOpenDialog(Repository.window) == JFileChooser.APPROVE_OPTION) {                    
            Repository.emptySuites();
            sc.g.setUser(Repository.getUsersDirectory()+Repository.getBar()+
                                        chooser.getSelectedFile().getName());
            sc.g.parseXML(chooser.getSelectedFile());
            if(Repository.getSuiteNr() > 0)sc.g.updateLocations(Repository.getSuita(0));
            sc.g.repaint();}}
        
    /*
     * save suite file on local PC
     */    
    private void saveLocalXML(){
        if(!sc.g.getUser().equals("")){//if there is an opened file
            try{JFileChooser chooser = new JFileChooser(); 
                chooser.setApproveButtonText("Save");
                chooser.setCurrentDirectory(new java.io.File("."));
                chooser.setDialogTitle("Choose Location");         
                chooser.setAcceptAllFileFilterUsed(false);    
                if (chooser.showOpenDialog(Panel1.this) == JFileChooser.APPROVE_OPTION) {
                    if(sc.g.printXML(chooser.getSelectedFile()+".xml", false,true,false,false,"")){
                        CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, Panel1.this,
                                                "Success","File successfully saved ");}
                    else{
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
                                                Panel1.this, "Warning",
                                                "Warning, file not saved.");}}
                else {System.out.println("No Selection");}}
            catch(Exception e){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
                                    Panel1.this, "Warning","Warning, file not saved.");
                System.out.println("There was a problem in writing xml file,"+
                                    " make sure file it is not in use.");
                e.printStackTrace();}}}
      
    /*
     * get first item selected
     */    
    private Item getItem(){
        ArrayList<Integer> temp = new ArrayList<Integer>();
        int indexsize = sc.g.getSelectedCollection().get(0).length;
        for(int j=0;j<indexsize;j++){
            temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));}
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
    /*    
     * add new suite file
     */        
    private void addSuiteFile(){
        String user = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
                                                    sc.g, "File Name", "Please enter file name").toUpperCase();
        if(user!=null){
            (new XMLBuilder(Repository.getSuite())).writeXMLFile(Repository.getUsersDirectory()+
                                                                System.getProperty("file.separator")+
                                                                user+".xml",false,false);
            Repository.window.mainpanel.p1.sc.g.setUser(Repository.getUsersDirectory()+
                                                                System.getProperty("file.separator")+
                                                                user+".xml");
            sc.g.printXML(sc.g.getUser(),false,false,false,false,"");
            sc.g.updateScroll();
            sc.g.repaint();
            Repository.window.mainpanel.p1.suitaDetails.setPreScript("");
            Repository.window.mainpanel.p1.suitaDetails.setPostScript("");
            Repository.window.mainpanel.p1.suitaDetails.setGlobalLibs(null);
            Repository.window.mainpanel.p1.suitaDetails.setDelay("");
            Repository.window.mainpanel.p1.suitaDetails.setStopOnFail(false);
            Repository.window.mainpanel.p1.suitaDetails.setSaveDB(false);
            Repository.emptySuites();
        
        
        }}
    
    /*
     * open existing suite file
     */
//     private void openSuiteFile(){
//         File usersdirectory = new File(Repository.getUsersDirectory());
//         String users[] = new String[usersdirectory.list().length];
//         System.arraycopy(usersdirectory.list(), 0, users, 0, usersdirectory.list().length);
//         JComboBox combo = new JComboBox(users);
//         int resp = (Integer)CustomDialog.showDialog(combo,JOptionPane.INFORMATION_MESSAGE,
//                                                     JOptionPane.OK_CANCEL_OPTION,sc.g,
//                                                     "Select project file",null);
//         if(resp==JOptionPane.OK_OPTION){
//             String user = combo.getSelectedItem().toString();
//             Repository.emptySuites();
//             Repository.window.mainpanel.p1.sc.g.setUser(Repository.getUsersDirectory()+
//                                                         Repository.getBar()+user);
//             Repository.window.mainpanel.p1.sc.g.parseXML(new File(Repository.getUsersDirectory()+
//                                                                     Repository.getBar()+user));}
//         if(Repository.getSuiteNr() > 0){
//             Repository.window.mainpanel.p1.sc.g.updateLocations(Repository.getSuita(0));}
//         Repository.window.mainpanel.p1.sc.g.repaint();}
        
    /*
     * set EP for selected
     * suite
     */    
    private void setEP(){
        try{final Item theone = getItem();
            /*
             * get EP's from EP's file
             */
            
//             File f = new File(Repository.temp+System.getProperty("file.separator")+
//                             "Twister"+System.getProperty("file.separator")+"EpID.txt");
//             String line = null;  
//             InputStream in = Repository.c.get(Repository.REMOTEEPIDDIR);
//             InputStreamReader inputStreamReader = new InputStreamReader(in);
//             BufferedReader bufferedReader = new BufferedReader(inputStreamReader);  
//             StringBuffer b=new StringBuffer("");
//             while ((line=bufferedReader.readLine())!= null){b.append(line+";");}                        
//             bufferedReader.close();
//             inputStreamReader.close();
//             in.close();
//             String result = b.toString();
//             String  [] vecresult = result.split(";");//EP's list


                StringBuilder b = new StringBuilder();
                Node parentnode = Repository.window.mainpanel.p4.getTB().getParentNode();
                HashMap children =  parentnode.getChildren();
                if(children!=null&&children.size()!=0){
                    Set keys = children.keySet();
                    Iterator iter = keys.iterator();
                    while(iter.hasNext()){
                        String n = iter.next().toString();
                        String name = parentnode.getChild(n).getName();
                        b.append(name);
                        b.append(";");
                    }
                }
                String [] vecresult = b.toString().split(";");   



                //String  [] vecresult = Repository.getRemoteFileContent(Repository.REMOTEEPIDDIR).split("\n");
            
            
//             try{JComboBox combo = new JComboBox(vecresult);
//                 int resp = (Integer)CustomDialog.showDialog(combo,JOptionPane.INFORMATION_MESSAGE,
//                                                             JOptionPane.OK_CANCEL_OPTION,sc.g,
//                                                             "Please select an Ep name",null);
//                 if(resp==JOptionPane.OK_OPTION){
//                     String ID = combo.getSelectedItem().toString();
//                     theone.setEpId(ID);
//                     for(int i=0;i<theone.getSubItemsNr();i++){
//                         sc.g.assignEpID(theone.getSubItem(i),ID);}
//                     repaint();}}
            try{JList combo = new JList(vecresult);
                
                String [] strings = theone.getEpId();
                ArrayList<String> array = new ArrayList<String>(Arrays.asList(vecresult));
                int [] sel = new int[strings.length];
                for(int i=0;i<strings.length;i++){
                    sel[i]=array.indexOf(strings[i]);
                }
                
                
                combo.setSelectedIndices(sel);
                
                
                int resp = (Integer)CustomDialog.showDialog(new JScrollPane(combo),JOptionPane.INFORMATION_MESSAGE,
                                                            JOptionPane.OK_CANCEL_OPTION,sc.g,
                                                            "Please select TB to run on",null);
                if(resp==JOptionPane.OK_OPTION){
                    String [] selected = new String[combo.getSelectedValuesList().size()];
                    for(int i=0;i<combo.getSelectedValuesList().size();i++){
                        selected[i] = combo.getSelectedValuesList().get(i).toString();
                    }
                    theone.setEpId(selected);
                    suitaDetails.combo.setSelectedIndices(combo.getSelectedIndices());
                    repaint();}}
            catch(Exception e){e.printStackTrace();}}
        catch(Exception e){e.printStackTrace();}}
    
    /*
     * filename - the name of the file
     * to display in UI for info
     */    
    public void setOpenedfile(String filename){
        openedfile.setText("Project file: "+filename);}}
        
class TreeDropTargetListener implements DropTargetListener {
    private boolean applet;
    public TreeDropTargetListener(boolean applet){this.applet = applet;}
    public void dragEnter(DropTargetDragEvent dropTargetDragEvent){}
    public void dragExit(DropTargetEvent dropTargetEvent){}
    public void dragOver(DropTargetDragEvent dropTargetDragEvent) {
        Grafic g = Repository.window.mainpanel.p1.sc.g;
        if(!g.getOnlyOptionals()){
            g.handleDraggingLine((int)dropTargetDragEvent.getLocation().getX(),
                                 (int)dropTargetDragEvent.getLocation().getY());
        }
    }
    public void dropActionChanged(DropTargetDragEvent dropTargetDragEvent){}
    public synchronized void drop(DropTargetDropEvent dropTargetDropEvent){
        Grafic g = Repository.window.mainpanel.p1.sc.g;
        try{g.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
            if(!g.getOnlyOptionals()){
                g.clearDraggingLine();
                g.drop((int)dropTargetDropEvent.getLocation().getX(),
                       (int)dropTargetDropEvent.getLocation().getY());
            }
        }
        catch(Exception e){
            e.printStackTrace();
            System.out.println("Could not get folder location");}}}
