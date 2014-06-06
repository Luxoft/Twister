/*
File: Panel1.java ; This file is part of Twister.
Version: 2.0031

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
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.event.MenuListener;
import java.io.File;
import javax.swing.JDialog;
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
import javax.swing.JButton;
import java.awt.Toolkit;
import javax.swing.JLabel;
import javax.swing.JFileChooser;
import javax.swing.event.MenuEvent;
import java.util.ArrayList;
import java.awt.FontMetrics;
import java.awt.Font;
import javax.swing.JTextField;
import javax.swing.ImageIcon;
import javax.swing.ToolTipManager;
import com.twister.Item;
import java.awt.Cursor;
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
import java.awt.dnd.DnDConstants;
import java.util.UUID;

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
    public JMenuBar menu;
    public Dependency dependency;
    private JTabbedPane optionstabs;
    
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
                generate(false);}});
        this.applet = applet;
        menu = new JMenuBar();
        menu.setLayout(null);
        menu.setBounds(0, 0, width, 20);
        JMenu filemenu = new JMenu("File");
        filemenu.setBounds(10,0,40,20);
        JMenuItem item = new JMenuItem("New project files");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addSuiteFile();}});
        filemenu.add(item);
        if(!PermissionValidator.canCreateProject()){
            item.setEnabled(false);
        }
        item = new JMenuItem("Open project file");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                RunnerRepository.openProjectFile();
            }});
        filemenu.add(item);
        item = new JMenuItem("Save project file");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveSuiteFile();}});
        filemenu.add(item);
        if(!PermissionValidator.canChangeProject()){
            item.setEnabled(false);
        }
        item = new JMenuItem("Save project as");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveSuiteAs();}});
        filemenu.add(item);
        if(!PermissionValidator.canCreateProject()){
            item.setEnabled(false);
        }
        item = new JMenuItem("Save for CLI");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                generate(true);}});
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
        item = new JMenuItem("Delete project file");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                deleteSuiteFile();}});
        filemenu.add(item);
        if(!PermissionValidator.canDeleteProject()){
            item.setEnabled(false);
        }
        item = new JMenuItem("Open from local");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                openLocalFile();}});
        filemenu.add(item);
        item = new JMenuItem("Save to local");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev){
                saveLocalXML();}});
        filemenu.add(item);
        if(!PermissionValidator.canCreateProject()){
            item.setEnabled(false);
        }
        menu.add(filemenu);
        final JMenu suitemenu = new JMenu("Suite");
        suitemenu.setBounds(50,0,50,20);
        menu.add(suitemenu);
        item = new JMenuItem("Add Suite");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.addSuiteFromButton();}});
        suitemenu.add(item);
        item = new JMenuItem("Expand");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                expandContract(true);}});
        item = new JMenuItem("Contract");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                expandContract(false);}});
        item = new JMenuItem("Export");
        suitemenu.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sc.g.exportSuiteToPredefined(getItem());}});
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
        add(menu);
        tdtl = new TreeDropTargetListener();        
        sc = new ScrollGrafic(10, 32, tdtl, user, applet);
        ep = new ExplorerPanel(applet);
        lp = new LibrariesPanel();
        setLayout(null); 
        tabs = new JTabbedPane();
        tabs.add("Test Case", ep);
        tabs.add("Predefined Suites", new JScrollPane(lp.tree));
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
        dependency = new Dependency();
        optionstabs = new JTabbedPane();
        optionstabs.add("Selection Options", suitaDetails);
        optionstabs.add("Dependencies", dependency);
        splitPane3 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                                                sc.pane,optionstabs);
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
                if(sc.g.printXML(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"Users"+RunnerRepository.getBar()+user+".xml",
                             false,false,
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
     * generate opened project file
     * and save it for CLI
     */
    private void saveForCLI(){
        final JTextField tf = new JTextField();
        JButton ok = new JButton("OK");
        JButton cancel = new JButton("Cancel");
        final JDialog dialog = CustomDialog.getDialog(tf, new JButton[]{ok,cancel},
                                                    JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION,
                                                    RunnerRepository.window,
                                                    "Please enter file name", null);
        dialog.addWindowListener(new WindowAdapter(){
          public void windowClosing(WindowEvent e){
              tf.setText("");
          }
        });
        ok.addActionListener(new ActionListener() {
          @Override
          public void actionPerformed(ActionEvent arg0) {
              dialog.setVisible(false);
              dialog.dispose();
          }
        });
        cancel.addActionListener(new ActionListener() {
          @Override
          public void actionPerformed(ActionEvent arg0) {
              tf.setText("");
              dialog.setVisible(false);
              dialog.dispose();
          }
        });
        dialog.setVisible(true);          
        String user = tf.getText();
        if(user!=null&&!user.equals("")){
            if(user.toLowerCase().indexOf(".xml")!=-1){
                int index = user.toLowerCase().indexOf(".xml");
                user = user.substring(0, index);
            }
            user+=".xml";
                          
            XMLBuilder xml = new XMLBuilder(RunnerRepository.getSuite());
            xml.createXML(true,suitaDetails.stopOnFail(),suitaDetails.preStopOnFail(),false,
                          RunnerRepository.window.mainpanel.p1.suitaDetails.getPreScript(),
                          RunnerRepository.window.mainpanel.p1.suitaDetails.getPostScript(),
                          suitaDetails.saveDB(),suitaDetails.getDelay(),RunnerRepository.window.mainpanel.p1.suitaDetails.getGlobalLibs(),
                          RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs());
            xml.skip = false;//must set to true to save generate file as suite file
            if(xml.writeXMLFile(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"Users"+RunnerRepository.getBar()+user,
                             false, false, false)){
                    CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, 
                                            RunnerRepository.window, "Success",
                                            "File successfully saved");
            } else {CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                            RunnerRepository.window, "Warning", 
                                            "Warning, file not saved");
            }
        }
    }
    
    
    /*
     * save opened project file
     * on server with name provided by user
     */
    private void saveSuiteAs(){
            final JTextField tf = new JTextField();
            JButton ok = new JButton("OK");
            JButton cancel = new JButton("Cancel");
            final JDialog dialog = CustomDialog.getDialog(tf, new JButton[]{ok,cancel},
                                                        JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION,
                                                        RunnerRepository.window,
                                                        "Please enter project file name", null);
            dialog.addWindowListener(new WindowAdapter(){
              public void windowClosing(WindowEvent e){
                  tf.setText("");
              }
            });
            ok.addActionListener(new ActionListener() {
              @Override
              public void actionPerformed(ActionEvent arg0) {
                  dialog.setVisible(false);
                  dialog.dispose();
              }
            });
            cancel.addActionListener(new ActionListener() {
              @Override
              public void actionPerformed(ActionEvent arg0) {
                  tf.setText("");
                  dialog.setVisible(false);
                  dialog.dispose();
              }
            });
            dialog.setVisible(true);          
            String user = tf.getText();
        
//            String user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
//                                                   JOptionPane.OK_CANCEL_OPTION, RunnerRepository.window,
//                                                   "File Name", "Please enter project file name");
            
            if(user!=null&&!user.equals("")){
                if(user.toLowerCase().indexOf(".xml")!=-1){
                    int index = user.toLowerCase().indexOf(".xml");
                    user = user.substring(0, index);
                }
                user+=".xml";
                if(!PermissionValidator.canChangeProject()){
                    for(String st:RunnerRepository.getProjectsFiles()){
                        if(st.equals(user)){
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                                RunnerRepository.window, "Warning",
                                                "File already exists, override not allowed, please enter different name.");
                            return;
                        }
                    }
                }
                if(sc.g.printXML(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"Users"+RunnerRepository.getBar()+user
                             ,false,false,
                             RunnerRepository.window.mainpanel.p1.suitaDetails.stopOnFail(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.preStopOnFail(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.saveDB(),
                             RunnerRepository.window.mainpanel.p1.suitaDetails.getDelay(),false,null,RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs())){
                    CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, 
                                            RunnerRepository.window, "Success",
                                            "File successfully saved");
                    //open new saved file
                    sc.g.setUser(user);//just need to rename to new file name
                }
                else {CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                            RunnerRepository.window, "Warning", 
                                            "Warning, file not saved");}}
                                        }
        
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
        Item theone = getItem();
        int nr = theone.getSubItemsNr();
        for(int i=0;i<nr;i++){
            theone.getSubItem(i).setVisible(expand);}
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
                        tcmenu.getMenuComponent(5).setEnabled(false);}
                    else tcmenu.getMenuComponent(4).setEnabled(false);}}}}
                    
    public void edit(boolean openlast){
        final int loc = splitPane3.getDividerLocation();
        splitPane3.setLeftComponent(sc.pane);
        optionstabs.insertTab("Selection Options", null, suitaDetails, null, 0);
        optionstabs.setSelectedIndex(0);
        splitPane3.setRightComponent(optionstabs);
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
                String content = new String(RunnerRepository.readProjectFile(user));
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
    private void generate(boolean cli){
        //check CE has clients started
        try{
            String resp = RunnerRepository.getRPCClient().execute("hasClients", new Object[]{RunnerRepository.user}).toString();
            if(resp=="false"){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, RunnerRepository.window,
                                        "ERROR","There are no clients started, please start client to run tests.");
                return;
            }
        } catch (Exception e){
            e.printStackTrace();
        }
        RunnerRepository.window.mainpanel.getP2().setSaveDB(suitaDetails.saveDB());
        int defsNr = suitaDetails.getDefsNr();
        boolean execute=true;
         /*
          * check if mandatory fields are set
          */
        for(int i=0;i<RunnerRepository.getSuiteNr();i++){
            for(int j=0;j<defsNr;j++){
                if( RunnerRepository.getDatabaseUserFields().get(j)[RunnerRepository.MANDATORY].equals("true") &&
                (RunnerRepository.getSuita(i).getUserDefNr()-1<j||RunnerRepository.getSuita(i).getUserDef(j)[1].length()==0)){
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, RunnerRepository.window,
                                            "Warning","Please set user defined field at "+
                                            RunnerRepository.getDatabaseUserFields().get(j)[RunnerRepository.LABEL]+
                                            " for: "+RunnerRepository.getSuita(i).getName());
                    execute = false;
                    return;}}
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
                return;
            }
        }
        /*
         * chech that there are tc'es to run
         */
        boolean found = false;
        for(Item i:RunnerRepository.getSuite()){
            if(i.getCheck()&&findRunnableTC(i)){
                found = true;
                break;
            }
        }
        if(!found){
            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, RunnerRepository.window,"Warning","Please add test cases to your suite");
            execute = false;
            return;
        }
        
        /*
         * check tc/suite for names
         */
        Item temp = null;
        for(Item i:RunnerRepository.getSuite()){
            temp = RunnerRepository.hasEmptyName(i);
            if(temp!=null){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, RunnerRepository.window,"ERROR","There is an item with an empty name, please set name!");
                execute = false;
                return;
            }
        }
        /*
         * check that SUT set on suites exist
         */
        String [] vecresult =  RunnerRepository.window.mainpanel.p4.getSut().sut.getSutTree().getSutsName();
        if(vecresult!=null){
            int size = vecresult.length;
            for(int i=0;i<size;i++){
                vecresult[i] = vecresult[i].replace(".user", "(user)");
                vecresult[i] = vecresult[i].replace(".system", "(system)");
            }
            for(Item i:RunnerRepository.getSuite()){
                found = false;
                for(String item:i.getEpId()){
                    for(String sut:vecresult){
                        if(item.equals(sut)){
                            found = true;
                        }
                    }
                    if(!found){
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, RunnerRepository.window,"Error","SUT file"+item+" cannot be read");
                        execute = false;
                        return;
                    }
                }
            }
        }
        
        /*
         * check all properties and parameters are valid
         */
        for(Item i:RunnerRepository.getSuite()){
            Item item = hasInvalidParams(i);
            if(item!=null){
                Item tcparent = sc.g.getTcParent(item,false);
                Item suiteparent = sc.g.getFirstSuitaParent(item,false);                
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, RunnerRepository.window,"Error","Please enter Name, and Value for all "+
                                                                                                  "Properties/Parameters on tc: "+tcparent.getName()+" on suite:"+suiteparent.getName());
                execute = false;
                return;
            }
        }
        
        /*
         * check dependencies
         */
        for(Item i:RunnerRepository.getSuite()){
            if(!checkDependency(i)){
                execute = false;
                return;
            }
        }
        
        if(execute){//all conditions are respected, start generating the file
            if(!cli){//if not for cli create last edited file
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
            }
            
            
            //duplicate repeating items
            ArrayList<Item> clone = new ArrayList<Item>();//array to hold the new created suites after duplicating
            for(Item i:RunnerRepository.getSuite()){
                multiplicateItem(i,clone);
            }
            
            //adjust items indexes in array
            for(Item i:clone){
                adjustIndex(i,clone.indexOf(i));
            }
            
            if(!cli){// if not for cli populate runner suite with the new created suites and continue generating file
                RunnerRepository.getSuite().clear();//populate the suites array with the new duplicated suites
                for(Item i:clone){
                    RunnerRepository.addSuita(i);
                }
                HashMap<String,ArrayList<Item>> duplicate = new HashMap();
                for(Item i:RunnerRepository.getSuite()){//store duplicates based on id
                    saveID(i,duplicate);
                }
                for(Item i:RunnerRepository.getSuite()){//remap dependencies
                    remapDependency(i,duplicate);
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
                new XMLReader(xml).parseXML(sc.g.getGraphics(), true,RunnerRepository.getTestSuite(),false);
                dependency.setParent(null);
                setRunning();
            } else {//cli file must be generated
                HashMap<String,ArrayList<Item>> duplicate = new HashMap();//store duplicates based on id
                for(Item i:clone){
                    saveID(i,duplicate);
                }   
                for(Item i:clone){//remap dependencies
                    remapDependency(i,duplicate);
                }
                
                final JTextField tf = new JTextField();
                JButton ok = new JButton("OK");
                JButton cancel = new JButton("Cancel");
                final JDialog dialog = CustomDialog.getDialog(tf, new JButton[]{ok,cancel},
                                                            JOptionPane.PLAIN_MESSAGE,
                                                            JOptionPane.OK_CANCEL_OPTION,
                                                            RunnerRepository.window,
                                                            "Please enter file name", null);
                dialog.addWindowListener(new WindowAdapter(){
                  public void windowClosing(WindowEvent e){
                      tf.setText("");
                  }
                });
                ok.addActionListener(new ActionListener() {
                  @Override
                  public void actionPerformed(ActionEvent arg0) {
                      dialog.setVisible(false);
                      dialog.dispose();
                  }
                });
                cancel.addActionListener(new ActionListener() {
                  @Override
                  public void actionPerformed(ActionEvent arg0) {
                      tf.setText("");
                      dialog.setVisible(false);
                      dialog.dispose();
                  }
                });
                dialog.setVisible(true);          
                String user = tf.getText();
                if(user!=null&&!user.equals("")){
                    if(user.toLowerCase().indexOf(".xml")!=-1){
                        int index = user.toLowerCase().indexOf(".xml");
                        user = user.substring(0, index);
                    }
                    user+=".xml";
                                  
                    XMLBuilder xml = new XMLBuilder(clone);
                    xml.createXML(true,suitaDetails.stopOnFail(),suitaDetails.preStopOnFail(),false,
                                  RunnerRepository.window.mainpanel.p1.suitaDetails.getPreScript(),
                                  RunnerRepository.window.mainpanel.p1.suitaDetails.getPostScript(),
                                  suitaDetails.saveDB(),suitaDetails.getDelay(),RunnerRepository.window.mainpanel.p1.suitaDetails.getGlobalLibs(),
                                  RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefs());
                    xml.skip = false;//must set to true to save generate file as suite file
                    if(xml.writeXMLFile(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"Users"+RunnerRepository.getBar()+user,
                                     false, false, false)){
                            CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE, 
                                                    RunnerRepository.window, "Success",
                                                    "File successfully saved");
                    } else {CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                                    RunnerRepository.window, "Warning", 
                                                    "Warning, file not saved");
                    }
                }                
            }
        }
    }
    
    private void printItems(Item item){
        System.out.println(item.getFileLocation());
        if(item.getType()==2){
            for(Item i:item.getSubItems()){
                printItems(i);
            }
        }
    }
    
    private void adjustIndex(Item i, int value){
        i.updatePos(i.getPos().size()-1, value);
        if(i.getType()==2){
            for(Item item: i.getSubItems()){
                adjustIndex(item,i.getSubItems().indexOf(item));
            }
        }        
    }
    
    private void remapDependency(Item i, HashMap<String,ArrayList<Item>> duplicates){
        if(i.getDependencies().size()>0){
            ArrayList<Item>torem = new ArrayList();
            HashMap<Item,String> add = new HashMap();
            for(Item dependency:i.getDependencies().keySet()){
                if(duplicates.get(dependency.getID())!=null && duplicates.get(dependency.getID()).size()>1){
                    String status = i.getDependencies().get(dependency);
                    //i.getDependencies().remove(dependency);
                    torem.add(dependency);
                    //check they are on the same suite
                    boolean onsamesuite = false;
                    for(Item duplicate:duplicates.get(dependency.getID())){
                        if(duplicate.getPos().get(0)==i.getPos().get(0)){
                            onsamesuite = true;
                            break;
                        }
                    }                    
                    if(!onsamesuite){//not on same suite, must add all dependencies
                        for(Item duplicate:duplicates.get(dependency.getID())){
                            //i.getDependencies().put(duplicate, status);
                            add.put(duplicate, status);
                            
                        }
                    }else { //on same suite, must add only the ones that are on same suite
                        for(Item duplicate:duplicates.get(dependency.getID())){
                            if(duplicate.getPos().get(0)==i.getPos().get(0)){
                                //i.getDependencies().put(duplicate, status);
                                add.put(duplicate, status);
                            }
                        }
                    }
                }
            }
            for(Item rem:torem){
                i.getDependencies().remove(rem);
            }
            for(Item dependency:add.keySet()){
                i.getDependencies().put(dependency, add.get(dependency));
            }
        }
        if(i.getType()==2){
            for(Item item:i.getSubItems()){
                remapDependency(item,duplicates);
            }
        }
    }
    
    private void printDependencySize(Item i){
        if(i.getType()==2){
            for(Item item:i.getSubItems()){
                printDependencySize(item);
            }
        }
    }
    
    private void saveID(Item i,HashMap<String,ArrayList<Item>> duplicate){
        ArrayList<Item> array = duplicate.get(i.getID());
        if(array==null){
            array = new ArrayList<Item>();
        }
        array.add(i);
        duplicate.put(i.getID(), array);
        i.setID(UUID.randomUUID().toString());//generate new ID for duplicated items
        if(i.getType()==2){
            for(Item item:i.getSubItems()){
                saveID(item,duplicate);
            }
        }
    }
    
    //manage duplicating items
    private void multiplicateItem(Item item, ArrayList<Item> array){
        ArrayList <Item> clonearray = new ArrayList();
        if(item.getRepeat()>1){
            for(int nr=0;nr<item.getRepeat();nr++){
                Item clone  = item.clone();
                for(Item i:item.getDependencies().keySet()){
                    clone.getDependencies().put(i, item.getDependencies().get(i));
                }
                if(clone.getType()==1){
                    ArrayList <Integer> indexpos3 = (ArrayList <Integer>)clone.getPos().clone();
                    indexpos3.add(new Integer(clone.getSubItemsNr()));
                    Item property = new Item("Iteration",0,-1,-1,0,20,indexpos3);
                    property.setValue(nr+1+"");
                    clone.addSubItem(property);
                }
                array.add(clone);
                if(clone.getType()==2){
                    clonearray.clear();
                    for(Item i:clone.getSubItems()){
                        multiplicateItem(i, clonearray);
                    }
                    clone.getSubItems().clear();
                    for(Item i:clonearray){
                        clone.addSubItem(i);
                    }
                }
            }
        } else {
//             array.add(item);
//             if(item.getType()==2){
//                 for(Item i:item.getSubItems()){
//                     multiplicateItem(i, clonearray);
//                 }
//                 item.getSubItems().clear();
//                 for(Item i:clonearray){
//                     item.addSubItem(i);
//                 }
//             }
            
            Item clone = item.clone();
            for(Item i:item.getDependencies().keySet()){
                clone.getDependencies().put(i, item.getDependencies().get(i));
            }
            array.add(clone);
            if(clone.getType()==2){
                for(Item i:clone.getSubItems()){
                    multiplicateItem(i, clonearray);
                }
                clone.getSubItems().clear();
                for(Item i:clonearray){
                    clone.addSubItem(i);
                }
            }
        }
    }
    
    
    
    private boolean checkDependency(Item current){
        HashMap <Item,String> hash = current.getDependencies();
        int currentindex = current.getPos().get(0);
        ArrayList<Integer> currentpos = current.getPos();
        for(Item dependency:hash.keySet()){
            if(dependency==null){
                System.out.println("ERROR! "+current.getFileLocation()+" has invalid dependecies in project");
                continue;
            }
            ArrayList<Integer> dependencypos = dependency.getPos();
            int dependencyidnex = dependency.getPos().get(0);  
            if(current.getType()==2){//check for dependency inside suite
                if(dependency.getPos().size()>current.getPos().size()){//check if tc could be inside suite
                    int size = currentpos.size();
                    boolean equals = true;
                    for(int i=0;i<size;i++){
                        if(currentpos.get(i)!=dependencypos.get(i)){//found different index, dependency is in different suite
                            equals = false;
                            break;
                        }
                    }
                    if(equals){
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, 
                                                RunnerRepository.window, "ERROR", 
                                                "Dependency is inside suite, please check order"); 
                        return false;
                    }
                }
            }
            if(dependencyidnex==currentindex){//in the same suite
                //check that dependency is after current
                int size = dependencypos.size();
                if(currentpos.size()<size) size = currentpos.size();
                for(int i=0;i<size;i++){
                    if(dependencypos.get(i)>currentpos.get(i)){
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, 
                                            RunnerRepository.window, "ERROR", 
                                            "Dependency is after tc: "+current.getFileLocation()+", please check order"); 
                        return false;
                    }
                }
            } else {//different suites
                
            }
        }
        for(Item subitem:current.getSubItems()){
            if(!checkDependency(subitem)){
                return false;
            }
        }
        return true;
    }
    
    /*
     * check if an item or subitem has 
     * parameters with name or value not set
     */
    private Item hasInvalidParams(Item item){
        if(item.getType()==2){
            for(Item i:item.getSubItems()){
                item = hasInvalidParams(i);
                if(item!=null){
                    return item;
                }
            }
        } else {
            int size = item.getSubItemsNr();
            for(Item i:item.getSubItems()){
                if(i.getName().equals("")||(!i.getName().equals("Running")&&i.getValue().equals(""))){
                    return i;  
                }
            }
        }
        return null;
    }
    
    
    
    
    /*
     * find if there is a tc set to be executed
     */
    private boolean findRunnableTC(Item i){
        if(i.getType()==1&&i.getCheck()){
            return true;
        }
        if(i.getType()==2&&i.getCheck()){
            for(int j=0;j<i.getSubItemsNr();j++){
                if(findRunnableTC(i.getSubItem(j))){
                    return true;
                }
            }
        }
        return false;
    }
    
    public void setRunning(){
        final int loc = splitPane3.getDividerLocation();
        splitPane3.setLeftComponent(RunnerRepository.window.mainpanel.getP2().sc.pane);
        splitPane3.setRightComponent(suitaDetails);
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
        suitaDetails.setEnabled(false);
        tcdetails.logs.doClick();
        RunnerRepository.window.mainpanel.getP2().play.doClick();
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
            try{RunnerRepository.deleteProjectFile(new File(sc.g.getUser()).getName());
                new File(sc.g.getUser()).delete();
            }
            catch(Exception e){e.printStackTrace();}}
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
            suitaDetails.setPreScript("");
            suitaDetails.setPostScript("");
            suitaDetails.setGlobalLibs(null);
            suitaDetails.setDelay("");
            suitaDetails.setStopOnFail(false);
            suitaDetails.setSaveDB(false);
            sc.g.getSelectedCollection().clear();
            RunnerRepository.emptySuites();
            
            sc.g.updateScroll();
            sc.g.repaint();
            RunnerRepository.window.mainpanel.p1.sc.g.setUser(RunnerRepository.getUsersDirectory()+
                                                                System.getProperty("file.separator")+
                                                                user+".xml");
            sc.g.printXML(sc.g.getUser(),false,false,false,false,false,"",false,null,null);
//             (new XMLBuilder(RunnerRepository.getSuite())).writeXMLFile(RunnerRepository.getUsersDirectory()+
//                                                                 System.getProperty("file.separator")+
//                                                                 user+".xml",false,false,false);
        }}
        
    /*
     * set EP for selected
     * suite
     */    
    private void setEP(){
        try{final Item theone = getItem();
            /*
             * get EP's from EP's file
             */
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
