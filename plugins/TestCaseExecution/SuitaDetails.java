/*
File: SuitaDetails.java ; This file is part of Twister.
Version: 2.0015

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
import javax.swing.JOptionPane;
import com.twister.Item;
import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import java.awt.Color;
import java.awt.BorderLayout;
import javax.swing.border.TitledBorder;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import java.awt.Dimension;
import java.util.ArrayList;
import java.awt.FontMetrics;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Component;
import java.util.List;
import org.apache.commons.vfs.FileObject;
import javax.swing.JFrame;
import javax.swing.JCheckBox;
import javax.swing.LayoutStyle;
import javax.swing.border.TitledBorder;
import javax.swing.JComboBox;
import javax.swing.DefaultComboBoxModel;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.event.KeyListener;
import javax.swing.JList;
import javax.swing.event.ListSelectionListener;
import javax.swing.event.ListSelectionEvent;
import java.util.Arrays;
import java.awt.Container;
import com.twister.MySftpBrowser;
import com.twister.CustomDialog;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;
import javax.swing.GroupLayout;
import javax.swing.SwingConstants;
import javax.swing.Box;
import javax.swing.event.DocumentListener;
import javax.swing.event.DocumentEvent;
import javax.swing.tree.DefaultMutableTreeNode;

public class SuitaDetails extends JPanel {
    private JPanel defsContainer,global, suiteoptions, tcoptions, summary;
    private JScrollPane scroll;
    private ArrayList <DefPanel> definitions = new ArrayList <DefPanel>();
    private TitledBorder border;    
    private JCheckBox stoponfail, runnable, optional, prerequisites,
                      savedb, panicdetect,teardown,prestoponfail;
    private JTextField tprescript, tpostscript,tview;
    private JButton browse1,browse2,suitelib;
    private Item parent;
    private JTextField tsuite,ttcname,ttcdelay;
    public JList combo;
    private JLabel ep, tcdelay;
    private JLabel stats [] = new JLabel[11];
    private String [] globallib;
    private PropPanel prop;
    private ParamPanel param;
    
    
    public void setEnabled(boolean enabled) {
        for (Component component : definitions)
            component.setEnabled(enabled);
        for (Component component : defsContainer.getComponents())
            component.setEnabled(enabled);
        for (Component component : global.getComponents())
            component.setEnabled(enabled);
        for (Component component : suiteoptions.getComponents())
            component.setEnabled(enabled);
        for (Component component : tcoptions.getComponents())
            component.setEnabled(enabled);
        combo.setEnabled(enabled);
        defsContainer.setEnabled(enabled);
        global.setEnabled(enabled);
        suiteoptions.setEnabled(enabled);
        tcoptions.setEnabled(enabled);
        if(enabled){
            if(getItemParent()==null){
                setTitle("Global options");
                scroll.setViewportView(global);
            } else if(getItemParent().getType()==2){
                setSuiteDetails(getItemParent().getPos().size()==1);
            } else if(getItemParent().getType()==1){
                setTCDetails();
            }
        } else {
            System.out.println(getPreferredSize().getWidth());
            setTitle("Summary");
            scroll.setViewportView(summary);
            revalidate();
            repaint();
        }
    }
    
    public void updateStats(int val[]){
        int i=0;
        for(JLabel l:stats){            
            l.setText(val[i]+"");
            i++;
        }
        summary.repaint();
    }
    
    public SuitaDetails(ArrayList<String []> descriptions) {
        initComponents(descriptions);}
        
    public void setTitle(String title){
        border.setTitle(title);
        repaint();}
        
    public void restart(ArrayList<String []> descriptions){
        removeAll();
        initComponents(descriptions);
        repaint();}
        
    private void initGlobal(){
        suiteoptions = new JPanel();
        suiteoptions.setBackground(Color.WHITE);
        JLabel suite = new JLabel("Suite name: ");
        tsuite = new JTextField();
        ep = new JLabel("Run on SUT:");
        combo = new JList();
        suitelib = new JButton("Libraries");
        panicdetect = new JCheckBox("Panic Detect");
        panicdetect.setBackground(Color.WHITE);
        
        JScrollPane scroll = new JScrollPane();
        scroll.setViewportView(combo);
        GroupLayout layout = new GroupLayout(suiteoptions);
        suiteoptions.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(panicdetect)
                    .addComponent(suitelib, GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(ep)
                    .addComponent(suite))
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(tsuite)
                    .addComponent(scroll, GroupLayout.DEFAULT_SIZE, 260, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(suite)
                    .addComponent(tsuite, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(10, 10, 10)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(scroll, GroupLayout.DEFAULT_SIZE, 96, Short.MAX_VALUE)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(panicdetect)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(suitelib))
                    .addComponent(ep))
                .addContainerGap())
        );
        tcdelay = new JLabel("TC delay");
        savedb = new JCheckBox("DB autosave");
        ttcdelay = new JTextField();
        JButton globallib = new JButton("Libraries");
        savedb.setBackground(Color.WHITE);
        stoponfail = new JCheckBox("Stop on fail");
        stoponfail.setBackground(Color.WHITE);
        JLabel prescript = new JLabel();
        JLabel postscript = new JLabel();
        prestoponfail = new JCheckBox("Stop on fail");
        prestoponfail.setBackground(Color.WHITE);
        tprescript = new JTextField();
        tpostscript = new JTextField();
        browse1 = new JButton("...");
        browse2 = new JButton("...");
        prescript.setText("Pre execution script:");
        postscript.setText("Post execution script:");
        
        globallib.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                showLib();
            }
        });
        
        suitelib.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                showSuiteLib();
            }
        });
        
        browse1.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {                            
                Container c;
                if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                else c = RunnerRepository.window;
                try{
                    new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tprescript,c,false);
                }catch(Exception e){
                    System.out.println("There was a problem in opening sftp browser!");
                    e.printStackTrace();
                }
            }
        });

        browse2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent evt) {
                Container c;
                if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                else c = RunnerRepository.window;
                try{
                    new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tpostscript,c,false);
                }catch(Exception e){
                    System.out.println("There was a problem in opening sftp browser!");
                    e.printStackTrace();
                }
            }
        });
        
        panicdetect.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent evt) {
                parent.setPanicdetect(panicdetect.isSelected());
            }
        });
        
        layout = new GroupLayout(global);
        global.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(stoponfail, GroupLayout.PREFERRED_SIZE, 105, GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(savedb, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(tcdelay)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(ttcdelay, GroupLayout.DEFAULT_SIZE, 160, Short.MAX_VALUE)
                        .addGap(12, 12, 12)
                        .addComponent(globallib))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(prescript)
                                .addGap(20, 20, 20))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                .addComponent(postscript)
                                .addGap(18, 18, 18)))
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(tpostscript)
                            .addComponent(tprescript))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(browse1)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(prestoponfail))
                            .addComponent(browse2))))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(12, 12, 12)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.CENTER)
                    .addComponent(stoponfail, GroupLayout.PREFERRED_SIZE, 20, GroupLayout.PREFERRED_SIZE)
                    .addComponent(savedb, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(tcdelay)
                    .addComponent(ttcdelay, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(globallib))
                .addGap(11, 11, 11)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(prescript)
                    .addComponent(tprescript, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(browse1)
                    .addComponent(prestoponfail))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(tpostscript, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(browse2)
                    .addComponent(postscript))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        layout.linkSize(SwingConstants.VERTICAL,
                        new Component[] {browse1, tprescript});

        layout.linkSize(SwingConstants.VERTICAL, 
                        new Component[] {browse2, tpostscript});
    }
    
    // show libraries selection window for root suite
    public void showSuiteLib(){
        JScrollPane jScrollPane1 = new JScrollPane();
        JList jList1 = new JList();
        JPanel libraries = new JPanel();
        jScrollPane1.setViewportView(jList1);
        GroupLayout layout = new GroupLayout(libraries);
        libraries.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE,
                            150, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE,
                            300, Short.MAX_VALUE)
        );
        
        try{Object [] s = (Object [])RunnerRepository.getRPCClient().execute("getLibrariesList",
                                                                        new Object[]{RunnerRepository.user});
            String [] libs = new String[s.length];
            for(int i=0;i<s.length;i++){
                libs[i] = s[i].toString();
            }
            ArrayList<Integer> ind = new ArrayList<Integer>();
            jList1.setModel(new DefaultComboBoxModel(libs));
            if(parent.getLibs()!=null){
                for(String st:parent.getLibs()){
                    for(int i=0;i<libs.length;i++){
                        if(libs[i].equals(st)){
                            ind.add(new Integer(i));
                        }
                    }
                }
                int [] indices = new int [ind.size()];
                for(int i=0;i<ind.size();i++){
                    indices[i]=ind.get(i);
                }
                jList1.setSelectedIndices(indices);
            }
        } catch(Exception e){
            System.out.println("There was an error on calling getLibrariesList on CE");
            e.printStackTrace();
        }
        int resp = (Integer)CustomDialog.showDialog(libraries,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Libraries",
                                                        null);
        if(resp == JOptionPane.OK_OPTION){
            Object[] val = jList1.getSelectedValues();
            String [] libs = new String[val.length];
            for(int s=0;s<val.length;s++){
                libs[s]=val[s].toString();
            }
            parent.setLibs(libs);
        }
    }
    
    // show libraries selection window for project 
    private void showLib(){
        JScrollPane jScrollPane1 = new JScrollPane();
        JList jList1 = new JList();
        JPanel libraries = new JPanel();
        jScrollPane1.setViewportView(jList1);
        GroupLayout layout = new GroupLayout(libraries);
        libraries.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 150, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 300, Short.MAX_VALUE)
        );
        
        try{Object [] s = (Object [])RunnerRepository.getRPCClient().execute("getLibrariesList",
                                                                        new Object[]{RunnerRepository.user});
            String [] libs = new String[s.length];
            for(int i=0;i<s.length;i++){
                libs[i] = s[i].toString();
            }
            ArrayList<Integer> ind = new ArrayList<Integer>();
            jList1.setModel(new DefaultComboBoxModel(libs));
            for(String st:globallib){
                for(int i=0;i<libs.length;i++){
                    if(libs[i].equals(st)){
                        ind.add(new Integer(i));
                    }
                }
            }
            int [] indices = new int [ind.size()];
            for(int i=0;i<ind.size();i++){
                indices[i]=ind.get(i);
            }
            jList1.setSelectedIndices(indices);
            
        } catch(Exception e){
            System.out.println("There was an error on calling getLibrariesList on CE");
            e.printStackTrace();
        }
        int resp = (Integer)CustomDialog.showDialog(libraries,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Libraries",
                                                        null);
        if(resp == JOptionPane.OK_OPTION){
            Object[] val = jList1.getSelectedValues();
            globallib = new String[val.length];
            for(int s=0;s<val.length;s++){
                globallib[s]=val[s].toString();
            }
        }
        
    }
    
    public String[] getGlobalLibs(){
        return globallib;
    }
    
    public void setGlobalLibs(String [] globallib){
        this.globallib = globallib;
    }
            
    private void initComponents(ArrayList<String []> descriptions){
        global = new JPanel();
        global.setBackground(Color.WHITE);
        initGlobal();
        initTCOptions();
        initSummary();
        definitions.clear();
        border = BorderFactory.createTitledBorder("Global options");
        setBorder(border);
        scroll = new JScrollPane();
//         setMinimumSize(new Dimension(10,10));
//         setMaximumSize(new Dimension(1000,1000));
//         setPreferredSize(new Dimension(100,100));
        defsContainer = new JPanel();
        setLayout(new BorderLayout());
        defsContainer.setBackground(Color.WHITE);
        defsContainer.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0));
        defsContainer.setLayout(new BoxLayout(defsContainer, BoxLayout.Y_AXIS));
        defsContainer.add(suiteoptions);
        scroll.setViewportView(global);
        add(scroll, BorderLayout.CENTER);
        JLabel l = new JLabel("test");            
        FontMetrics metrics = l.getFontMetrics(l.getFont());
        int width = 0;
        for(int i=0;i<descriptions.size();i++){
            if(width<metrics.stringWidth(descriptions.get(i)[RunnerRepository.LABEL])){
                width = metrics.stringWidth(descriptions.get(i)[RunnerRepository.LABEL]);
            }
        }
        for(int i=0;i<descriptions.size();i++){
            String button = descriptions.get(i)[RunnerRepository.SELECTED];
            DefPanel define = new DefPanel(descriptions.get(i)[RunnerRepository.LABEL],
                                                               button,
                                                               descriptions.get(i)[RunnerRepository.ID],
                                                               width,i,this);
            definitions.add(define);
            defsContainer.add(define);
        }
    }
    
    public void initSummary(){
        summary = new JPanel();
        summary.setBackground(Color.WHITE);
        summary.setPreferredSize(new Dimension(300,220));
        summary.setLayout(null);
        
        JLabel l1 = new JLabel("Total TC:");
        l1.setBounds(10,5,75,25);
        summary.add(l1);        
        stats[0] =  new JLabel();
        stats[0].setBounds(118,5,100,25);
        
        JLabel l4 = new JLabel("Pass:");
        l4.setBounds(10,22,40,25);
        summary.add(l4);
        stats[3] = new JLabel();
        stats[3].setBounds(118,22,100,25);
        
        JLabel l5 = new JLabel("Fail:");
        l5.setBounds(10,39,40,25);
        summary.add(l5);
        stats[4] = new JLabel();
        stats[4].setBounds(118,39,100,25);
         
        JLabel l3 = new JLabel("Running:");
        l3.setBounds(10,55,70,25);
        summary.add(l3);
        stats[2] = new JLabel();
        stats[2].setBounds(118,55,100,25);        
        
        JLabel l2 = new JLabel("Pending:");
        l2.setBounds(10,75,70,25);
        summary.add(l2);        
        stats[1] = new JLabel();
        stats[1].setBounds(118,75,100,25);

        JLabel l6 = new JLabel("Skipped:");
        l6.setBounds(10,95,70,25);
        summary.add(l6);
        stats[5] = new JLabel();
        stats[5].setBounds(118,95,100,25);

        JLabel l7 = new JLabel("Aborted:");
        l7.setBounds(10,115,70,25);
        summary.add(l7);
        stats[6] = new JLabel();
        stats[6].setBounds(118,115,100,25);

        JLabel l8 = new JLabel("Not Executed:");
        l8.setBounds(10,135,105,25);
        summary.add(l8);
        stats[7] = new JLabel();
        stats[7].setBounds(118,135,100,25);

        JLabel l9 = new JLabel("Timeout:");
        l9.setBounds(10,155,70,25);
        summary.add(l9);
        stats[8] = new JLabel();
        stats[8].setBounds(118,155,100,25);  
        
        JLabel l10 = new JLabel("Waiting:");
        l10.setBounds(10,175,60,25);
        summary.add(l10);
        stats[10] = new JLabel();
        stats[10].setBounds(118,175,100,25);
        
        JLabel l11 = new JLabel("Invalid:");
        l11.setBounds(10,195,60,25);
        summary.add(l11);
        stats[9] = new JLabel();
        stats[9].setBounds(118,195,100,25);

        for(JLabel l:stats){
            if(l!=null)summary.add(l);
        }
    }
    
    public void initTCOptions(){
        tcoptions = new JPanel();
        tcoptions.setBackground(Color.WHITE);
        JLabel tcname = new JLabel("TC name:");
        ttcname = new JTextField();
        JLabel view = new JLabel("TC view: ");
        tview = new JTextField();
        runnable = new JCheckBox("Runnable");
        runnable.setBackground(Color.WHITE);
        optional = new JCheckBox("Optional");
        optional.setBackground(Color.WHITE);
        prerequisites = new JCheckBox("setup file");
        teardown = new JCheckBox("teardown file");
        prerequisites.setBackground(Color.WHITE);
        teardown.setBackground(Color.WHITE);
        prop = new PropPanel();
        param = new ParamPanel();
        
        
        
        GroupLayout layout = new GroupLayout(tcoptions);
        tcoptions.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(
                layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(prop, 0, 0, Short.MAX_VALUE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(param, 0, 0, Short.MAX_VALUE))
                            .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                    .addGroup(layout.createSequentialGroup()
                                        .addComponent(runnable)
                                        .addGap(18, 18, 18)
                                        .addComponent(optional)
                                        .addGap(18, 18, 18)
                                        .addComponent(prerequisites)
                                        .addGap(18, 18, 18)
                                        .addComponent(teardown))
                                    .addGroup(layout.createSequentialGroup()
                                        .addComponent(tcname)
                                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(ttcname, GroupLayout.PREFERRED_SIZE, 300, GroupLayout.PREFERRED_SIZE))
                                    .addGroup(layout.createSequentialGroup()
                                        .addComponent(view)
                                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(tview, GroupLayout.PREFERRED_SIZE, 300, GroupLayout.PREFERRED_SIZE)))
                                .addGap(0, 0, Short.MAX_VALUE)))
                        .addContainerGap()))
                );
                
        layout.setVerticalGroup(
                layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                            .addComponent(tcname)
                            .addComponent(ttcname, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                            .addComponent(view)
                            .addComponent(tview, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                        
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                            .addComponent(runnable)
                            .addComponent(optional)
                            .addComponent(prerequisites)
                            .addComponent(teardown))
                        .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(prop, 0,0, Short.MAX_VALUE)
                            .addComponent(param, 0,0, Short.MAX_VALUE))
                        .addContainerGap())
                );
    }
           
    public int getDefsNr(){
        return definitions.size();}
        
    public ArrayList<DefPanel> getDefs(){
        return definitions;}
           
    public void clearDefs(){
        for(int i=0;i<definitions.size();i++){
            definitions.get(i).setDescription("",true);}}
       
    /*
     * set options according to new selected item
     */
    public void setParent(Item parent){ 
        //if(this.parent==parent)return;
        this.parent = parent;
        if(parent!=null&&parent.getType()==2){
            try{
                setComboTBs();
                tsuite.setText(parent.getName());
                KeyListener k [] = combo.getKeyListeners();
                for(KeyListener t : k){
                    tsuite.removeKeyListener(t);
                }
                tsuite.addKeyListener(new KeyAdapter(){
                    public void keyReleased(KeyEvent ev){
                        String name = tsuite.getText();
                        FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 14));
                        int width = metrics.stringWidth(name)+40;
                        getItemParent().setName(name);
                        getItemParent().getRectangle().setSize(width,(int)getItemParent().getRectangle().getHeight());
                        if(getItemParent().isVisible())RunnerRepository.window.mainpanel.p1.sc.g.updateLocations(getItemParent());
                        RunnerRepository.window.mainpanel.p1.sc.g.repaint();
                    }
                });
                panicdetect.setSelected(parent.isPanicdetect());
            } catch (Exception e){
                System.out.println("There was a problem in getting ep list");
                e.printStackTrace();
            }
            for(int i=0;i<definitions.size();i++){
                definitions.get(i).setParent(parent);
            }
        }
        if(parent!=null&&parent.getType()==1){
            if(parent.isRunnable())runnable.setSelected(true);
            else runnable.setSelected(false);
            if(parent.isOptional())optional.setSelected(true);
            else optional.setSelected(false);
            if(parent.isPrerequisite())prerequisites.setSelected(true);
            else prerequisites.setSelected(false);
            if(parent.isTeardown())teardown.setSelected(true);
            else teardown.setSelected(false);
            ttcname.setText(getItemParent().getName());
            if(parent.isClearcase()){
                tview.setText(ClearCase.getView());
            } else {
                tview.setText("");
            }
            KeyListener k [] = ttcname.getKeyListeners();
            for(KeyListener t : k){
                ttcname.removeKeyListener(t);
            }
            ttcname.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    String name = ttcname.getText();
                    FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 14));
                    int width = metrics.stringWidth(name)+20;
                    getItemParent().setName(name);
                    getItemParent().getRectangle().setSize(width,(int)getItemParent().getRectangle().getHeight());
                    if(getItemParent().isVisible())RunnerRepository.window.mainpanel.p1.sc.g.updateLocations(getItemParent());
                    RunnerRepository.window.mainpanel.p1.sc.g.repaint();
                }
            });
            ActionListener [] s = runnable.getActionListeners();
            for(ActionListener a:s){
                runnable.removeActionListener(a);
            }
            runnable.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    if(runnable.isSelected())getItemParent().setRunnable(true);
                    else getItemParent().setRunnable(false);
                    RunnerRepository.window.mainpanel.p1.sc.g.repaint();
                }
            });
            s = optional.getActionListeners();
            for(ActionListener a:s){
                optional.removeActionListener(a);
            }
            optional.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    if(optional.isSelected()){
                        getItemParent().setOptional(true);
                        RunnerRepository.window.mainpanel.p1.sc.g.unsetPrerequisite(getItemParent());
                        prerequisites.setSelected(false);
                    }
                    else getItemParent().setOptional(false);
                    RunnerRepository.window.mainpanel.p1.sc.g.repaint();
                }
            });
            s = prerequisites.getActionListeners();
            for(ActionListener a:s){
                prerequisites.removeActionListener(a);
            }
            prerequisites.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    if(prerequisites.isSelected()){
                        RunnerRepository.window.mainpanel.p1.sc.g.setPreRequisites(getItemParent());
                    }
                    else{
                        RunnerRepository.window.mainpanel.p1.sc.g.unsetPrerequisite(getItemParent());
                    }
                }
            });
            
            s = teardown.getActionListeners();
            for(ActionListener a:s){
                teardown.removeActionListener(a);
            }
            teardown.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    if(teardown.isSelected()){
                        //getItemParent().setPrerequisite(false);
                        RunnerRepository.window.mainpanel.p1.sc.g.setTeardown(getItemParent());
                    }
                    else{
                        RunnerRepository.window.mainpanel.p1.sc.g.unsetTeardown(getItemParent());
                    }
                }
            });
            prop.setParent(getItemParent());
            param.setParent(getItemParent());
        }
    }

    //update TB;s names in Suite Options
    //panel when there is a parent selected
    public void setComboTBs(){
        if(parent==null)return;
        for(ListSelectionListener l:combo.getListSelectionListeners()){
            combo.removeListSelectionListener(l);
        }
        StringBuilder b = new StringBuilder();
        DefaultMutableTreeNode root = RunnerRepository.window.mainpanel.p4.getSut().sut.root;
        int sutsnr = root.getChildCount();
        for(int i=0;i<sutsnr;i++){
            b.append(root.getChildAt(i).toString());
            b.append(";");
        }
        
        
        
//         StringBuilder b = new StringBuilder();
        
//         Node parentnode = RunnerRepository.window.mainpanel.p4.getTB().getParentNode();
//         HashMap children =  parentnode.getChildren();
//         if(children!=null&&children.size()!=0){
//             Set keys = children.keySet();
//             Iterator iter = keys.iterator();
//             while(iter.hasNext()){
//                 String n = iter.next().toString();
//                 String name = parentnode.getChild(n).getName();
//                 b.append(name);
//                 b.append(";");
//             }
//         }
        String [] vecresult = b.toString().split(";");
        
        
        combo.setModel(new DefaultComboBoxModel(vecresult));
        
        String [] strings = parent.getEpId();
        ArrayList<String> array = new ArrayList<String>(Arrays.asList(vecresult));
        int [] sel = new int[strings.length];
        for(int i=0;i<strings.length;i++){
            sel[i]=array.indexOf(strings[i]);
        }
        combo.setSelectedIndices(sel);
        combo.addListSelectionListener(new MyListSelectionListener());
        
        
    }

    public void setSuiteDetails(boolean rootsuite){
        if(rootsuite){
            combo.setEnabled(true);
            ep.setEnabled(true);
            suitelib.setEnabled(true);
            panicdetect.setEnabled(true);
            for(DefPanel p:definitions){
                defsContainer.add(p);
            }         
        } else {
            suitelib.setEnabled(false);
            panicdetect.setEnabled(false);
            combo.setEnabled(false);
            ep.setEnabled(false);
            for(DefPanel p:definitions){
                defsContainer.remove(p);
            }
        }
        scroll.setViewportView(defsContainer);
        setBorderTitle("Suite options");
    }

    public void setTCDetails(){
        scroll.setViewportView(tcoptions);
        setBorderTitle("TC options");
    }

    public void setGlobalDetails(){
        scroll.setViewportView(global);
        setBorderTitle("Global options");
    }
    
    public void setSummaryDetails(){
        scroll.setViewportView(summary);
        setBorderTitle("Summary");
    }

    public DefPanel getDefPanel(int i){
        return definitions.get(i);}
    
    public boolean stopOnFail(){
        return stoponfail.isSelected();}
        
    public boolean preStopOnFail(){
        return prestoponfail.isSelected();}
        
    public boolean saveDB(){
        return savedb.isSelected();}
        
    public void setStopOnFail(boolean value){
        stoponfail.setSelected(value);}
        
    public void setPreStopOnFail(boolean value){
        prestoponfail.setSelected(value);}
        
    public void setSaveDB(boolean value){
        savedb.setSelected(value);}
        
    public void setDelay(String delay){
        ttcdelay.setText(delay);}
    
    public String getDelay(){
        return ttcdelay.getText();}
        
    public void setPreScript(String script){
        tprescript.setText(script);}
        
    public void setPostScript(String script){
        tpostscript.setText(script);}
        
    public String getPreScript(){
        return tprescript.getText();}
        
    public String getPostScript(){
        return tpostscript.getText();}
        
    public void setBorderTitle(String title){
        ((TitledBorder)getBorder()).setTitle(title);
        repaint();
    }
    
    public Item getItemParent(){
        return this.parent;
    }
    
    class MyListSelectionListener implements ListSelectionListener {
        public void valueChanged(ListSelectionEvent evt) {
            if (!evt.getValueIsAdjusting()) {
                JList list = (JList)evt.getSource();
                String [] selected = new String[list.getSelectedValuesList().size()];
                for(int i=0;i<list.getSelectedValuesList().size();i++){
                    selected[i] = list.getSelectedValuesList().get(i).toString();
                }
                getItemParent().setEpId(selected);
                RunnerRepository.window.mainpanel.p1.sc.g.repaint();
            }
        }
    }  
}


class ParamPanel extends JPanel{
    private Item parent;
    private JPanel jPanel2,addpanel;
    
    public ParamPanel(){
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(153, 153, 153)),
                                                    "Parameters", TitledBorder.DEFAULT_JUSTIFICATION,
                                                    TitledBorder.DEFAULT_POSITION, null, new Color(0, 0, 0)));
        setBackground(Color.WHITE);
        jPanel2 = new JPanel();
        jPanel2.setBackground(Color.WHITE);
        JScrollPane jScrollPane3 = new JScrollPane(jPanel2);
        jScrollPane3.setBackground(Color.WHITE);
        jScrollPane3.setBorder(null);
        jPanel2.setLayout(new BoxLayout(jPanel2, BoxLayout.Y_AXIS));
        
        addpanel = new JPanel();
        addpanel.setMaximumSize(new Dimension(32767, 25));
        addpanel.setMinimumSize(new Dimension(0, 25));
        addpanel.setPreferredSize(new Dimension(50, 25));
        addpanel.setLayout(new BorderLayout());
        JButton add = new JButton("Add");
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                ArrayList <Integer> indexpos3 = (ArrayList <Integer>)parent.getPos().clone();
                indexpos3.add(new Integer(parent.getSubItemsNr()));
                Item property = new Item("param",0,-1,-1,10,20,indexpos3);
                property.setSubItemVisible(false);
                property.setValue("");
                parent.addSubItem(property);
                Param prop = new Param(parent,property);
                jPanel2.remove(addpanel);
                jPanel2.add(prop);
                jPanel2.add(addpanel);
                jPanel2.revalidate();
                jPanel2.repaint();
            }
        });
        addpanel.add(add,BorderLayout.EAST);
        addpanel.setBackground(Color.WHITE);
        GroupLayout paramLayout = new GroupLayout(this);
        this.setLayout(paramLayout);
        paramLayout.setHorizontalGroup(
            paramLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane3)
        );
        paramLayout.setVerticalGroup(
            paramLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane3)
        );
    }
    
    public void setParent(Item parent){
        //if(parent!=this.parent){
            this.parent = parent;
            initializeParent();
        //}
    }
    
    private void initializeParent(){
        jPanel2.removeAll();
        for(Item i:parent.getSubItems()){
            if(i.getName().equals("param")){
                Param param = new Param(parent,i);
                jPanel2.add(param);
            }
        }
        jPanel2.add(addpanel);
    }
    
    class Param extends JPanel{
        private Item parent,reference;
        
        public Param(final Item parent,final Item reference){
            this.reference = reference; 
            this.parent = parent;
            setMaximumSize(new Dimension(32767, 25));
            setMinimumSize(new Dimension(0, 25));
            setPreferredSize(new Dimension(50, 25));
            setBackground(Color.WHITE);
            setLayout(new BorderLayout(5,0));
            JLabel jLabel18 = new JLabel(" Parameter:");
            add(jLabel18, BorderLayout.WEST);
            final JTextField jTextField18 = new JTextField();
            jTextField18.setText(reference.getValue());
            jTextField18.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    reference.setValue(jTextField18.getText());
                }
            });
            add(jTextField18, BorderLayout.CENTER);
            JButton jButton10 = new JButton("Remove");
            jButton10.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    parent.getSubItems().remove(reference);
                    jPanel2.remove(Param.this);
                    jPanel2.repaint();
                    jPanel2.revalidate();
                }
            });
            add(jButton10, java.awt.BorderLayout.EAST);
        }
    }
    
}

class PropPanel extends JPanel{
    private Item parent;
    private JPanel jPanel1,addpanel;
    
    public PropPanel(){
        jPanel1 = new JPanel();
        addpanel = new JPanel();
        addpanel.setMaximumSize(new Dimension(32767, 25));
        addpanel.setMinimumSize(new Dimension(0, 25));
        addpanel.setPreferredSize(new Dimension(50, 25));
        addpanel.setLayout(new BorderLayout());
        JButton add = new JButton("Add");
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                ArrayList <Integer> indexpos3 = (ArrayList <Integer>)parent.getPos().clone();
                indexpos3.add(new Integer(parent.getSubItemsNr()));
                Item property = new Item("",0,-1,-1,10,20,indexpos3);
                property.setSubItemVisible(false);
                property.setValue("");
                parent.addSubItem(property);
                Prop prop = new Prop(parent,property);
                jPanel1.remove(addpanel);
                jPanel1.add(prop);
                jPanel1.add(addpanel);
                jPanel1.revalidate();
                jPanel1.repaint();
            }
        });
        addpanel.add(add,BorderLayout.EAST);
        addpanel.setBackground(Color.WHITE);
        JScrollPane jScrollPane1 = new JScrollPane(jPanel1);
        jPanel1.setBackground(Color.WHITE);
        jScrollPane1.setBackground(Color.WHITE);
        jScrollPane1.setBorder(null);
        jPanel1.setLayout(new BoxLayout(jPanel1, BoxLayout.Y_AXIS));
        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(153, 153, 153)),
                                                    "Properties", TitledBorder.DEFAULT_JUSTIFICATION,
                                                    TitledBorder.DEFAULT_POSITION, null, new Color(0, 0, 0)));
        setBackground(Color.WHITE);
        GroupLayout propLayout = new GroupLayout(this);
        setLayout(propLayout);
        propLayout.setHorizontalGroup(
            propLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1)
        );
        propLayout.setVerticalGroup(
            propLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1)
        );
    }
    
    public void setParent(Item parent){
        //if(parent!=this.parent){
            this.parent = parent;
            initializeParent();
        //}
    }
    
    private void initializeParent(){
        jPanel1.removeAll();
        System.out.println(parent.getName()+" : "+parent.getSubItemsNr());
        for(Item i:parent.getSubItems()){
            if((!i.getName().equals("Running"))&&(!i.getName().equals("param"))){
                Prop prop = new Prop(parent,i);
                jPanel1.add(prop);
            }
        }
        jPanel1.add(addpanel);
    }
    
    class Prop extends JPanel{
        private Item parent,reference;
        
        public Prop(final Item parent,final Item reference){
            this.reference = reference;
            this.parent = parent;
            setMaximumSize(new Dimension(32767, 25));
            setMinimumSize(new Dimension(0, 25));
            setPreferredSize(new Dimension(50, 25));
            setBackground(Color.WHITE);
            setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
            JLabel jLabel1 = new JLabel(" Name: ");
            final JTextField jTextField1 = new JTextField();
            jTextField1.setText(reference.getName());
            jTextField1.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    reference.setName(jTextField1.getText());
                    jTextField1.setPreferredSize(new Dimension(25,20));
                }
            });
            JLabel jLabel2 = new JLabel(" Value: ");
            final JTextField jTextField2 = new JTextField();
            jTextField2.setText(reference.getValue());
            jTextField2.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    reference.setValue(jTextField2.getText());
                    jTextField2.setPreferredSize(new Dimension(25,20));
                }
            });
            JButton jButton1 = new JButton("Remove");
            jButton1.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    parent.getSubItems().remove(reference);
                    jPanel1.remove(Prop.this);
                    jPanel1.repaint();
                    jPanel1.revalidate();
                }
            });
            add(jLabel1);
            add(jTextField1);
            add(jLabel2);
            add(jTextField2);
            add(Box.createRigidArea(new Dimension(5, 0)));
            add(jButton1);
        }
    }
    
}
        
class DefPanel extends JPanel{
    private JLabel description;
    private JPanel filedsGap;
    private JTextField userDefinition;
    private int index;
    private Item parent;
    private SuitaDetails container;
    private DefPanel reference;
    private String id;
    private String descriptions;
    private DocumentListener doclistener;
    
    public DefPanel(String descriptions,String button,String id, 
                    int width,final int index, SuitaDetails container){
        this.descriptions = descriptions;
        this.id = id;
        reference = this;
        this.container = container;
        this.index = index;
        setBackground(new Color(255, 255, 255));
        setBorder(BorderFactory.createEmptyBorder(2, 20, 2, 20));
        setMaximumSize(new Dimension(32767, 30));
        setMinimumSize(new Dimension(100, 30));
        setPreferredSize(new Dimension(300, 30));
        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        description = new JLabel(descriptions);
        description.setPreferredSize(new Dimension(width,20));
        description.setMinimumSize(new Dimension(width,20));        
        description.setMaximumSize(new Dimension(width,20));
        add(description);
        filedsGap = new JPanel();
        filedsGap.setBackground(new Color(255, 255, 255));
        filedsGap.setMaximumSize(new Dimension(20, 20));
        filedsGap.setMinimumSize(new Dimension(20, 20));
        filedsGap.setPreferredSize(new Dimension(20, 20));
        GroupLayout filedsGapLayout = new GroupLayout(filedsGap);
        filedsGap.setLayout(filedsGapLayout);
        filedsGapLayout.setHorizontalGroup(filedsGapLayout.
                                           createParallelGroup(GroupLayout.Alignment.LEADING).
                                           addGap(0, 20, Short.MAX_VALUE));
        filedsGapLayout.setVerticalGroup(filedsGapLayout.
                                        createParallelGroup(GroupLayout.Alignment.LEADING).
                                        addGap(0, 20, Short.MAX_VALUE));
        add(filedsGap);        
        userDefinition = new JTextField();
        doclistener = new DocumentListener() {
            public void changedUpdate(DocumentEvent e) {
                setParentField(userDefinition.getText(),false);
            }
            public void removeUpdate(DocumentEvent e) {
                setParentField(userDefinition.getText(),false);
            }
            public void insertUpdate(DocumentEvent e) {
                setParentField(userDefinition.getText(),false);
            }
        };
        userDefinition.getDocument().addDocumentListener(doclistener);
        userDefinition.setText("");
        userDefinition.setMaximumSize(new Dimension(300, 100));
        userDefinition.setMinimumSize(new Dimension(50, 20));
        userDefinition.setPreferredSize(new Dimension(100, 20));
        add(userDefinition);
        filedsGap = new JPanel();
        filedsGap.setBackground(new Color(255, 255, 255));
        filedsGap.setMaximumSize(new Dimension(20, 20));
        filedsGap.setMinimumSize(new Dimension(20, 20));
        filedsGap.setPreferredSize(new Dimension(20, 20));
        filedsGapLayout = new GroupLayout(filedsGap);
        filedsGap.setLayout(filedsGapLayout);
        filedsGapLayout.setHorizontalGroup(filedsGapLayout.
                                           createParallelGroup(GroupLayout.Alignment.LEADING).
                                           addGap(0, 20, Short.MAX_VALUE));
        filedsGapLayout.setVerticalGroup(filedsGapLayout.
                                         createParallelGroup(GroupLayout.Alignment.LEADING).
                                         addGap(0, 20, Short.MAX_VALUE));
        add(filedsGap);
        if(button.equals("UserSelect")){
            final JButton database = new JButton("Database");
            database.setMaximumSize(new Dimension(100, 20));
            database.setMinimumSize(new Dimension(50, 20));
            database.setPreferredSize(new Dimension(80, 20));
            add(database);
            database.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    DatabaseFrame frame = new DatabaseFrame(reference);
                    frame.executeQuery();
                    frame.setLocation((int)database.getLocationOnScreen().getX()-100,
                                      (int)database.getLocationOnScreen().getY());
                    frame.setVisible(true);}});}
        else if(button.equals("UserScript")){
            JButton script = new JButton("Script");
            script.setMaximumSize(new Dimension(100, 20));
            script.setMinimumSize(new Dimension(50, 20));
            script.setPreferredSize(new Dimension(80, 20));
            add(script);
            script.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    Container c;
                    if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                    else c = RunnerRepository.window;
                    try{
//                         String passwd = RunnerRepository.getRPCClient().execute("sendFile", new Object[]{"/etc/passwd"}).toString();
//                         new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,userDefinition,c,passwd);
                        new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,userDefinition,c,false);
                    }catch(Exception e){
                            System.out.println("There was a problem in opening sftp browser!");
                            e.printStackTrace();
                        }
                    }});
            filedsGap = new JPanel();
            filedsGap.setBackground(new Color(255, 255, 255));
            filedsGap.setMaximumSize(new Dimension(10, 10));
            filedsGap.setMinimumSize(new Dimension(10, 10));
            filedsGap.setPreferredSize(new Dimension(10, 10));    
            filedsGapLayout = new GroupLayout(filedsGap);
            filedsGap.setLayout(filedsGapLayout);
            filedsGapLayout.setHorizontalGroup(filedsGapLayout.
                                               createParallelGroup(GroupLayout.Alignment.LEADING).
                                               addGap(0, 20, Short.MAX_VALUE));
            filedsGapLayout.setVerticalGroup(filedsGapLayout.
                                             createParallelGroup(GroupLayout.Alignment.LEADING).
                                             addGap(0, 20, Short.MAX_VALUE));
            filedsGap.setLayout(filedsGapLayout);           
            add(filedsGap); 
            final JButton value = new JButton("Value");
            value.setMaximumSize(new Dimension(100, 20));
            value.setMinimumSize(new Dimension(50, 20));
            value.setPreferredSize(new Dimension(80, 20));
            add(value);
            value.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    String script = userDefinition.getText();
                    if(script!=null && !script.equals("")){
                        try{
                            String result = RunnerRepository.getRPCClient().execute("runUserScript",
                                                                     new Object[]{script})+"";
                            JFrame f = new JFrame();
                            f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
                            f.setLocation(value.getLocationOnScreen());
                            JLabel l = new JLabel("Script result: "+result);
                            f.getContentPane().add(l, BorderLayout.CENTER);
                            f.pack();
                            f.setVisible(true);
                        }
                        catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                }});
            }
        else if(button.equals("UserText")){
            JPanel database = new JPanel();
            database.setBackground(Color.WHITE);
            database.setMaximumSize(new Dimension(100, 20));
            database.setMinimumSize(new Dimension(50, 20));
            database.setPreferredSize(new Dimension(80, 20));
            add(database);}}
                
    public void setEnabled(boolean enabled) {
        super.setEnabled(enabled);
        for (Component component : getComponents())
            component.setEnabled(enabled);}
    
    public void setParentField(String def,boolean updateField){
//         for (StackTraceElement ste : Thread.currentThread().getStackTrace()) {
//             System.out.println(ste);
//         }


//         System.out.println(parent.getName()+" "+userDefinition.getText());
        if(updateField)userDefinition.setText(def);
        parent.setUserDef(index,id,def);}
        
    public String getFieldID(){
        return id;}
                
    protected void setParent(Item parent){
        if(parent!=null&&parent.getType()==2){
            container.setTitle("Suite options");
            container.setEnabled(true);}
        else{
            container.setTitle("Global options");}
        this.parent = parent;}
        
    public String getDescription(){
        return descriptions;}
    
    public void setDescription(String desc, boolean removelistener){
        if(removelistener){
            userDefinition.getDocument().removeDocumentListener(doclistener);
        }
        userDefinition.setText(desc);
        if(removelistener){
            userDefinition.getDocument().addDocumentListener(doclistener);
        }
    }}   