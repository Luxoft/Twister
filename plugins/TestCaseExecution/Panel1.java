/*
File: Panel1.java ; This file is part of Twister.
Version: 2.0018

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
import java.awt.datatransfer.StringSelection;
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
import javax.swing.JTabbedPane;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.dnd.DnDConstants;
import javax.swing.tree.DefaultMutableTreeNode;

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
    public LibrariesPanel lp;
    public ClearCasePanel cp;
    public JTabbedPane tabs;
    
    public Panel1(String user, final boolean applet, int width){
        RunnerRepository.introscreen.setStatus("Started Suites interface initialization");
        RunnerRepository.introscreen.addPercent(0.035);
        RunnerRepository.introscreen.repaint();
        openedfile = new JLabel();
        openedfile.setBounds(410,22,250,20);
        add(openedfile);
        addsuite = new JButton(new ImageIcon(RunnerRepository.addsuitaicon));
        addsuite.setToolTipText("Add Suite");
        ToolTipManager.sharedInstance().setInitialDelay(400);
        addsuite.setBounds(10,20,40,25);
        add(addsuite);
        addsuite.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.addSuiteFromButton();}});        
        remove = new JButton(new ImageIcon(RunnerRepository.removeicon));
        remove.setToolTipText("Remove");
        remove.setBounds(52,20,40,25);
        remove.setEnabled(false);
        add(remove);
        remove.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.removeSelected();}});
        generate = new JButton("Run",new ImageIcon(RunnerRepository.getPlayIcon()));
        generate.setBounds(94,20,105,25);
        generate.setToolTipText("Run suite");
        if(!PermissionValidator.canRunTests()){
            JButton temp = new JButton("Run",new ImageIcon(RunnerRepository.getPlayIcon()));
            temp.setBounds(94,20,105,25);
            temp.setToolTipText("Run suite");
            add(temp);
            temp.setEnabled(false);
        } else {
            add(generate);
        }
        showoptionals = new JButton("Show optionals");
        showoptionals.setBounds(205,20,150,25);
        showoptionals.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                showOptionals();}});
        add(showoptionals);
        suitaDetails = new SuitaDetails(RunnerRepository.getDatabaseUserFields(),RunnerRepository.getProjectUserFields());
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
        item = new JMenuItem("New project file");
//         JMenuItem newuser = new JMenuItem("New project file");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addSuiteFile();}});
        filemenu.add(item);
        if(!PermissionValidator.canCreateProject()){
            item.setEnabled(false);
        }
//         JMenuItem changeuser = new JMenuItem("Open project file");
        item = new JMenuItem("Open project file");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                RunnerRepository.openProjectFile();
            }});
        filemenu.add(item);
//         JMenuItem saveuser = new JMenuItem("Save project file");
        item = new JMenuItem("Save project file");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveSuiteFile();}});
        filemenu.add(item);
        if(!PermissionValidator.canChangeProject()){
            item.setEnabled(false);
        }
        
//         JMenuItem saveuseras = new JMenuItem("Save project as");
        item = new JMenuItem("Save project as");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveSuiteAs();}});
        filemenu.add(item);
        if(!PermissionValidator.canCreateProject()){
            item.setEnabled(false);
        }
        item = new JMenuItem("Export project");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                exportAsSuite();}});
        filemenu.add(item);
        if(!PermissionValidator.canCreateProject()){
            item.setEnabled(false);
        }
//         JMenuItem deleteuser = new JMenuItem("Delete project file");
        item = new JMenuItem("Delete project file");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                deleteSuiteFile();}});
        filemenu.add(item);
        if(!PermissionValidator.canDeleteProject()){
            item.setEnabled(false);
        }
//         JMenuItem openlocalXML = new JMenuItem("Open from local");
        item = new JMenuItem("Open from local");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                openLocalFile();}});
        filemenu.add(item);
//         JMenuItem savelocalXML = new JMenuItem("Save to local");
        item = new JMenuItem("Save to local");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveLocalXML();}});
        filemenu.add(item);
        if(!PermissionValidator.canCreateProject()){
            item.setEnabled(false);
        }
        menu.add(filemenu);
        add(menu);
        tdtl = new TreeDropTargetListener();        
        sc = new ScrollGrafic(10, 32, tdtl, user, applet);
        ep = new ExplorerPanel(applet);
        lp = new LibrariesPanel();
        //cp = new ClearCasePanel();
        //ep = new ExplorerPanel(470, 32, tdtl, applet, RunnerRepository.c);
        setLayout(null); 
        tabs = new JTabbedPane();
        tabs.add("Test Case", new JScrollPane(ep.tree));
        tabs.add("Predefined Suites", new JScrollPane(lp.tree));
        //tabs.add("ClearCase Tests", new JScrollPane(cp.tree));
        splitPane2 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                                                tabs,
                                                tcdetails);
        try{
            SwingUtilities.invokeLater(new Runnable() {
                public void run(){
                    splitPane2.setDividerLocation(RunnerRepository.getLayouts().
                                                 get("mainh2splitlocation").getAsInt());
                }
            });
        } catch(Exception e){
            splitPane2.setDividerLocation(0.5);
        }           
        splitPane3 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                                                sc.pane,suitaDetails);
//         splitPane3 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
//                                                 new JScrollPane(),suitaDetails);
        try{
            SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    splitPane3.setDividerLocation(RunnerRepository.getLayouts().
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
                    splitPane.setDividerLocation(RunnerRepository.getLayouts().
                                                 get("mainvsplitlocation").getAsInt());
                }
            });
        } catch(Exception e){
            splitPane.setDividerLocation(0.5);
        }
        add(splitPane);
        RunnerRepository.introscreen.setStatus("Finished Suites interface initialization");
        RunnerRepository.introscreen.addPercent(0.035);
        RunnerRepository.introscreen.repaint();
        edit = new JButton("Edit");
        edit.setBounds(10,20,65,25);
        edit.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                edit(true);}});}
        
        
    /*
     * method to show optionals tc
     * in suites tab
     */
    public void showOptionals(){
        boolean show;
        if(RunnerRepository.getSuiteNr()>0){
            if(showoptionals.getText().equals("Show optionals")){
                showoptionals.setText("Show all");
                sc.g.setOnlyOptionals(true);
                sc.g.showOptionals(null);
                sc.g.updateLocations(RunnerRepository.getSuita(0));
                sc.g.repaint();
                return;
            }
            showoptionals.setText("Show optionals");
                sc.g.setOnlyOptionals(false);
                sc.g.showOptionals(null);
                sc.g.updateLocations(RunnerRepository.getSuita(0));
                sc.g.repaint();
                return;
    }}
    
    
    /*
     * save opened project file
     * on server with name provided by user
     * as suite file
     */
    private void exportAsSuite(){
        if(!sc.g.getUser().equals("")){
            String user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, RunnerRepository.window,
                                                    "File Name", "Please enter suite file name");
            
            if(user!=null&&!user.equals("")){
                if(sc.g.printXML(user+".xml", false,false,
                             RunnerRepository.window.mainpanel.p1.suitaDetails.stopOnFail(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.preStopOnFail(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.saveDB(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.getDelay(),true,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs())){
                    CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, 
                                            RunnerRepository.window, "Success",
                                            "File successfully saved");
                    lp.refreshTree(100,100);
                }
                    
                else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                            RunnerRepository.window, "Warning", 
                                            "Warning, file not saved");}}
        
    }
    
    
    /*
     * save opened project file
     * on server with name provided by user
     */
    private void saveSuiteAs(){
            String user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, RunnerRepository.window,
                                                    "File Name", "Please enter project file name");
            
            if(user!=null&&!user.equals("")){
                if(user.toLowerCase().indexOf(".xml")!=-1){
                    int index = user.toLowerCase().indexOf(".xml");
                    user = user.substring(0, index);
                }
                user+=".xml";
                if(!PermissionValidator.canChangeProject()){
                    String [] files = RunnerRepository.getRemoteFolderContent(RunnerRepository.getRemoteUsersDirectory());
                    for(String st:files){
                        if(st.equals(user)){
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                                RunnerRepository.window, "Warning",
                                                "File already exists, override not allowed, please enter different name.");
                            return;
                        }
                    }
                }
                if(sc.g.printXML(user, false,false,
                             RunnerRepository.window.mainpanel.p1.suitaDetails.stopOnFail(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.preStopOnFail(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.saveDB(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.getDelay(),false,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs()))
                    CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, 
                                            RunnerRepository.window, "Success",
                                            "File successfully saved");
                else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                            RunnerRepository.window, "Warning", 
                                            "Warning, file not saved");}}
//                                         }
        
    /*
     * save opened suite file
     * on server
     */
    private void saveSuiteFile(){
        if(sc.g.getUser()!=null&&!sc.g.getUser().equals("")){
            if(sc.g.printXML(sc.g.getUser(), false,false,
                             RunnerRepository.window.mainpanel.p1.suitaDetails.stopOnFail(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.preStopOnFail(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.saveDB(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.getDelay(),
                             false,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs()))
                CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, 
                                        RunnerRepository.window, "Success",
                                        "File successfully saved");
            else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                        RunnerRepository.window, "Error", 
                                        "Error, file not saved");}}
        
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
                RunnerRepository.getSuite().remove(theone);                    
                if(RunnerRepository.getSuiteNr()>=index){
                    for(int i= index;i<RunnerRepository.getSuiteNr();i++){
                        RunnerRepository.getSuita(i).updatePos(0,
                                    new Integer(RunnerRepository.getSuita(i).
                                    getPos().get(0).intValue()-1));}
                if(RunnerRepository.getSuiteNr()>0){
                    RunnerRepository.getSuita(0).setLocation(new int[]{5,10});
                    sc.g.updateLocations(RunnerRepository.getSuita(0));}
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
                                                    sc.g, "TC Name", "Please enter the TC name");
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
                                                    "Suite Name", "Please enter the suite name");
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
                    
    public void edit(boolean openlast){
        final int loc = splitPane3.getDividerLocation();
        splitPane3.setLeftComponent(sc.pane);
//         JScrollPane sp = new JScrollPane();
//         sp.setPreferredSize(new Dimension(800,600));
//         splitPane3.setLeftComponent(sp);
        try{
            SwingUtilities.invokeLater(new Runnable(){
                public void run() {
                    splitPane3.setDividerLocation(loc);
                }
            });
        } catch(Exception e){
            splitPane3.setDividerLocation(0.5);
        }   
        remove(edit);
        remove(RunnerRepository.window.mainpanel.getP2().play);
        remove(RunnerRepository.window.mainpanel.getP2().stop);        
        remove(RunnerRepository.window.mainpanel.getP2().cestatus); 
        add(openedfile);
        add(remove);
        add(generate);
        add(showoptionals);
        add(addsuite);
        suitaDetails.setEnabled(true);
        tcdetails.tcdetails.doClick();
        RunnerRepository.emptySuites();
        if(openlast){
            try{
                String user = "last_edited.xml";
                if(RunnerRepository.window.mainpanel.p1.sc.g.getUser()==null&&
                   RunnerRepository.window.mainpanel.p1.sc.g.getUser().equals("")){
                      RunnerRepository.window.mainpanel.p1.sc.g.setUser(RunnerRepository.getUsersDirectory()+
                                                                    RunnerRepository.getBar()+user);
                }
                File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"Users"+RunnerRepository.getBar()+user);
                BufferedWriter writer = new BufferedWriter(new FileWriter(file));
                String content = new String(RunnerRepository.getRemoteFileContent(RunnerRepository.getRemoteUsersDirectory()+"/"+user,false));
                writer.write(content);
                writer.close();
                RunnerRepository.window.mainpanel.p1.sc.g.parseXML(new File(RunnerRepository.getUsersDirectory()+
                                                                              RunnerRepository.getBar()+user));
            } catch (Exception e){
                e.printStackTrace();
            }
            
        }
        if(RunnerRepository.getSuiteNr() > 0){
            RunnerRepository.window.mainpanel.p1.sc.g.updateLocations(RunnerRepository.getSuita(0));}
        RunnerRepository.window.mainpanel.p1.suitaDetails.setGlobalDetails();
        RunnerRepository.window.mainpanel.p1.sc.g.repaint();
        repaint();
    }    
       
    /*
     * generate master suites XML
     */
    private void generate(){
        RunnerRepository.window.mainpanel.getP2().setSaveDB(suitaDetails.saveDB());
        int defsNr = suitaDetails.getDefsNr();
        boolean execute=true;
        for(int i=0;i<RunnerRepository.getSuiteNr();i++){
            /*
             * check if mandatory fields are set
             */
            for(int j=0;j<defsNr;j++){
                if( RunnerRepository.getDatabaseUserFields().get(j)[RunnerRepository.MANDATORY].equals("true") &&
                (RunnerRepository.getSuita(i).getUserDefNr()-1<j||RunnerRepository.getSuita(i).getUserDef(j)[1].length()==0)){
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, RunnerRepository.window,
                                            "Warning","Please set user defined field at "+
                                            RunnerRepository.getDatabaseUserFields().get(j)[RunnerRepository.LABEL]+
                                            " for: "+RunnerRepository.getSuita(i).getName());
                    execute = false;
                    break;}}
        }
        
        /*
         * check if mandatory project fields are set
         */
        ArrayList<String[]> databaseuserfields = RunnerRepository.getProjectUserFields();
        String [][] projectdefined =  suitaDetails.getProjectDefs();
        for(int i=0;i<databaseuserfields.size();i++){
            if(databaseuserfields.get(i)[RunnerRepository.MANDATORY].equals("true")&&(projectdefined[i][1]==null||projectdefined[i][1].equals(""))){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, RunnerRepository.window,
                                        "Warning","Please set project defined field for "+projectdefined[i][2]);
                execute = false;
                break;
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
                                 suitaDetails.preStopOnFail(),
                                 suitaDetails.saveDB(),
                                 suitaDetails.getDelay(),false,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs())){}
                else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                            RunnerRepository.window, "Warning", 
                                            "Warning, temp file not saved");                    
            }
            if(!sc.g.printXML(RunnerRepository.getTestXMLDirectory(),true,false,
                          suitaDetails.stopOnFail(),suitaDetails.preStopOnFail(),suitaDetails.saveDB(),
                          suitaDetails.getDelay(),false,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs())){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, 
                                            RunnerRepository.window, "ERROR", 
                                            "Could not generate XML, please check log!");  
                return;
            }
            RunnerRepository.emptyTestRunnerRepository();
            File xml = new File(RunnerRepository.getTestXMLDirectory());
            int size = RunnerRepository.getLogs().size();
            for(int i=5;i<size;i++){RunnerRepository.getLogs().remove(5);}
//             new XMLReader(xml).parseXML(sc.g.getGraphics(), true);
            new XMLReader(xml).parseXML(sc.g.getGraphics(), true,RunnerRepository.getTestSuite(),false);
            setRunning();
        }
    }
    
    public void setRunning(){
        final int loc = splitPane3.getDividerLocation();
        splitPane3.setLeftComponent(RunnerRepository.window.mainpanel.getP2().sc.pane);
//         JScrollPane sp = new JScrollPane();
//         sp.setPreferredSize(new Dimension(800,600));
//         splitPane3.setLeftComponent(sc);
        try{
            SwingUtilities.invokeLater(new Runnable(){
                public void run() {
                    splitPane3.setDividerLocation(loc);
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
        add(RunnerRepository.window.mainpanel.getP2().play);
        add(RunnerRepository.window.mainpanel.getP2().stop);        
        add(RunnerRepository.window.mainpanel.getP2().cestatus);
        RunnerRepository.window.mainpanel.getP2().play.doClick();
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
            RunnerRepository.emptySuites();
            try{new File(sc.g.getUser()).delete();
                if(!RunnerRepository.removeRemoteFile(RunnerRepository.getRemoteUsersDirectory()+"/"+(new File(sc.g.getUser()).getName()))){
                    System.out.println("Could not delete "+new File(sc.g.getUser()).getName()+
                                        " from "+RunnerRepository.getRemoteUsersDirectory());
                }
//                 try{RunnerRepository.c.cd(RunnerRepository.getRemoteUsersDirectory());
//                     RunnerRepository.c.rm(new File(sc.g.getUser()).getName());}
//                 catch(Exception e){
//                     System.out.println("Could not delete "+new File(sc.g.getUser()).getName()+
//                                         " from "+RunnerRepository.getRemoteUsersDirectory());
//                     e.printStackTrace();}
            }
            catch(Exception e){e.printStackTrace();}
//             File usersdirectory = new File(RunnerRepository.getUsersDirectory());
//             String users[] = new String[usersdirectory.list().length + 1];
//             System.arraycopy(usersdirectory.list(), 0, users, 0, usersdirectory.list().length);
//             users[users.length - 1] = "New File";
//             JComboBox combo = new JComboBox(users);
//             int resp = (Integer)CustomDialog.showDialog(combo,JOptionPane.INFORMATION_MESSAGE,
//                                                         JOptionPane.OK_CANCEL_OPTION,Panel1.this,
//                                                         "File Name",null);
//             if(resp==JOptionPane.OK_OPTION){
//                 String user = combo.getSelectedItem().toString();
//                 if(user.equals("New File")){
//                     user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
//                                                         Panel1.this, "File Name", "Please enter file name");
//                     if(!user.equals("NULL")){
//                         RunnerRepository.emptySuites();
//                         sc.g.getSelectedCollection().clear();
//                         (new XMLBuilder(RunnerRepository.getSuite())).writeXMLFile((new StringBuilder()).
//                                                                append(RunnerRepository.getUsersDirectory()).
//                                                                append(System.getProperty("file.separator"))
//                                                                .append(user).append(".xml").toString(),false,false,false);
//                         sc.g.setUser((new StringBuilder()).append(RunnerRepository.getUsersDirectory()).
//                                                                     append(System.getProperty("file.separator")).
//                                                                     append(user).append(".xml").toString());
//                         sc.g.printXML(sc.g.getUser(),false,false,false,false,"",false,null);}}
//                 else if(user != null){
//                     sc.g.setUser((new StringBuilder()).append(RunnerRepository.getUsersDirectory()).
//                                                                 append(System.getProperty("file.separator")).
//                                                                 append(user).toString());
//                     sc.g.parseXML(new File((new StringBuilder()).append(RunnerRepository.getUsersDirectory()).
//                                                                 append(System.getProperty("file.separator")).
//                                                                 append(user).toString()));}}
//             else RunnerRepository.window.mainpanel.p1.sc.g.setUser("");
//             if(RunnerRepository.getSuiteNr() > 0)RunnerRepository.window.mainpanel.p1.sc.g.updateLocations(RunnerRepository.getSuita(0));
//             RunnerRepository.window.mainpanel.p1.sc.g.repaint();
//             RunnerRepository.window.mainpanel.p1.sc.g.repaint();
        }
            RunnerRepository.openProjectFile();
        
        
    }
        
    /*
     * open XML file from
     * local PC
     */    
    private void openLocalFile(){
        JFileChooser chooser = new JFileChooser(); 
        chooser.setFileFilter(new XMLFilter());
        chooser.setCurrentDirectory(new java.io.File("."));
        chooser.setDialogTitle("Select XML File"); 
        if (chooser.showOpenDialog(RunnerRepository.window) == JFileChooser.APPROVE_OPTION) {                    
            RunnerRepository.emptySuites();
            sc.g.setUser(RunnerRepository.getUsersDirectory()+RunnerRepository.getBar()+
                                        chooser.getSelectedFile().getName());
            sc.g.parseXML(chooser.getSelectedFile());
            if(RunnerRepository.getSuiteNr() > 0)sc.g.updateLocations(RunnerRepository.getSuita(0));
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
                    if(sc.g.printXML(chooser.getSelectedFile()+".xml", false,true,false,false,false,"",false,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs())){
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
                generate.setToolTipText("Run suite");}}}
    /*    
     * add new suite file
     */        
    private void addSuiteFile(){
        String user = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
                                                    sc.g, "File Name", "Please enter file name");
        if(user!=null){
            (new XMLBuilder(RunnerRepository.getSuite())).writeXMLFile(RunnerRepository.getUsersDirectory()+
                                                                System.getProperty("file.separator")+
                                                                user+".xml",false,false,false);
            RunnerRepository.window.mainpanel.p1.sc.g.setUser(RunnerRepository.getUsersDirectory()+
                                                                System.getProperty("file.separator")+
                                                                user+".xml");
            sc.g.printXML(sc.g.getUser(),false,false,false,false,false,"",false,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs());
            sc.g.updateScroll();
            sc.g.repaint();
            suitaDetails.setPreScript("");
            suitaDetails.setPostScript("");
            suitaDetails.setGlobalLibs(null);
            suitaDetails.setDelay("");
            suitaDetails.setStopOnFail(false);
            suitaDetails.setSaveDB(false);
            sc.g.getSelectedCollection().clear();
            RunnerRepository.emptySuites();
        
        
        }}
    
    /*
     * open existing suite file
     */
//     private void openSuiteFile(){
//         File usersdirectory = new File(RunnerRepository.getUsersDirectory());
//         String users[] = new String[usersdirectory.list().length];
//         System.arraycopy(usersdirectory.list(), 0, users, 0, usersdirectory.list().length);
//         JComboBox combo = new JComboBox(users);
//         int resp = (Integer)CustomDialog.showDialog(combo,JOptionPane.INFORMATION_MESSAGE,
//                                                     JOptionPane.OK_CANCEL_OPTION,sc.g,
//                                                     "Select project file",null);
//         if(resp==JOptionPane.OK_OPTION){
//             String user = combo.getSelectedItem().toString();
//             RunnerRepository.emptySuites();
//             RunnerRepository.window.mainpanel.p1.sc.g.setUser(RunnerRepository.getUsersDirectory()+
//                                                         RunnerRepository.getBar()+user);
//             RunnerRepository.window.mainpanel.p1.sc.g.parseXML(new File(RunnerRepository.getUsersDirectory()+
//                                                                     RunnerRepository.getBar()+user));}
//         if(RunnerRepository.getSuiteNr() > 0){
//             RunnerRepository.window.mainpanel.p1.sc.g.updateLocations(RunnerRepository.getSuita(0));}
//         RunnerRepository.window.mainpanel.p1.sc.g.repaint();}
        
    /*
     * set EP for selected
     * suite
     */    
    private void setEP(){
        try{final Item theone = getItem();
            /*
             * get EP's from EP's file
             */
            
//             File f = new File(RunnerRepository.temp+System.getProperty("file.separator")+
//                             "Twister"+System.getProperty("file.separator")+"EpID.txt");
//             String line = null;  
//             InputStream in = RunnerRepository.c.get(RunnerRepository.REMOTEEPIDDIR);
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
                Node parentnode = RunnerRepository.window.mainpanel.p4.getTB().getParentNode();
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



                //String  [] vecresult = RunnerRepository.getRemoteFileContent(RunnerRepository.REMOTEEPIDDIR).split("\n");
            
            
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
    public void dragEnter(DropTargetDragEvent dropTargetDragEvent){}
    public void dragExit(DropTargetEvent dropTargetEvent){}
    public void dragOver(DropTargetDragEvent dropTargetDragEvent) {
        Grafic g = RunnerRepository.window.mainpanel.p1.sc.g;
        if(!g.getOnlyOptionals()){
            g.handleDraggingLine((int)dropTargetDragEvent.getLocation().getX(),
                                 (int)dropTargetDragEvent.getLocation().getY());
        }
    }
    public void dropActionChanged(DropTargetDragEvent dropTargetDragEvent){}
    public synchronized void drop(DropTargetDropEvent dropTargetDropEvent){
        
        try{dropTargetDropEvent.acceptDrop(DnDConstants.ACTION_COPY_OR_MOVE);
            String str = (String) dropTargetDropEvent.getTransferable().getTransferData(DataFlavor.stringFlavor);
            Grafic g = RunnerRepository.window.mainpanel.p1.sc.g;
            if(str.equals("lib")){//drop called from libs
                try{g.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
                    if(!g.getOnlyOptionals()){
                        g.clearDraggingLine();
                        g.drop((int)dropTargetDropEvent.getLocation().getX(),
                               (int)dropTargetDropEvent.getLocation().getY(),"lib");
                    }
                }
                catch(Exception e){
                    e.printStackTrace();
                    System.out.println("Could not get folder location");
                }
            } else if(str.equals("tc")){//drop called from tc
                System.out.println("tc");
                try{g.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
                    if(!g.getOnlyOptionals()){
                        g.clearDraggingLine();
                        g.drop((int)dropTargetDropEvent.getLocation().getX(),
                               (int)dropTargetDropEvent.getLocation().getY(),"tc");
                    }
                }
                catch(Exception e){
                    e.printStackTrace();
                    System.out.println("Could not get folder location");}
            } else if(str.equals("clearcase")){//drop called from clearcase
                System.out.println("clearcase");
                try{g.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
                    if(!g.getOnlyOptionals()){
                        g.clearDraggingLine();
                        g.drop((int)dropTargetDropEvent.getLocation().getX(),
                               (int)dropTargetDropEvent.getLocation().getY(),"clearcase");
                    }
                }
                catch(Exception e){
                    e.printStackTrace();
                    System.out.println("Could not get folder location");}
            }
            
            
        } catch (Exception e){
            e.printStackTrace();
        }
        
        }}
