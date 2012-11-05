/*
File: SuitaDetails.java ; This file is part of Twister.

Copyright (C) 2012 , Luxoft

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
import javax.swing.GroupLayout;
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
import java.util.ArrayList;
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

public class SuitaDetails extends JPanel {
    private JPanel defsContainer,global, suiteoptions, tcoptions, summary;
    private JScrollPane scroll;
    private ArrayList <DefPanel> definitions = new ArrayList <DefPanel>();
    private TitledBorder border;    
    private JCheckBox stoponfail, runnable, optional, prerequisites, savedb;
    private JTextField tprescript, tpostscript;
    private JButton browse1,browse2;
    private Item parent;
    private JTextField tsuite,ttcname,ttcdelay;
    private JList combo;
    private JLabel ep, tcdelay;
    private JLabel stats [] = new JLabel[10];
    
    public void setEnabled(boolean enabled) {
        //super.setEnabled(enabled);
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
        ep = new JLabel("Run on EP:");
        combo = new JList();
        
        JScrollPane scroll = new JScrollPane();
        scroll.setViewportView(combo);
        GroupLayout layout = new GroupLayout(suiteoptions);
        suiteoptions.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(21, 21, 21)
                .addComponent(suite)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(tsuite, javax.swing.GroupLayout.PREFERRED_SIZE, 145, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(ep)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(scroll, 60, 70, 100)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(suite)
                    .addComponent(tsuite, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(ep)
                    .addComponent(scroll, 60, 70, 100))
                .addContainerGap())
        );
        tcdelay = new JLabel("TC delay");
        savedb = new JCheckBox("DB autosave");
        ttcdelay = new JTextField();
        savedb.setBackground(Color.WHITE);
        stoponfail = new JCheckBox("Stop on fail");
        stoponfail.setBackground(Color.WHITE);
        JLabel prescript = new JLabel();
        JLabel postscript = new JLabel();
        tprescript = new JTextField();
        tpostscript = new JTextField();
        browse1 = new JButton("...");
        browse2 = new JButton("...");

//         stoponfail.setText();
        prescript.setText("Pre execution script:");
        postscript.setText("Post execution script:");
        
        browse1.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
//                 if(fileChooser==null)initializeFileBrowser();
//                 try{RETURN_TYPE answer = fileChooser.showOpenDialog(SuitaDetails.this);
//                     if (answer == RETURN_TYPE.APPROVE){
//                         FileObject aFileObject = fileChooser.getSelectedFile();
//                         String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
//                         safeName = safeName.substring(safeName.indexOf(Repository.host)+
//                                                         Repository.host.length());
//                         String [] check = safeName.split("/");
//                         if(check[check.length-1].equals(check[check.length-2])){
//                             StringBuffer buffer = new StringBuffer();
//                             for(int i=0;i<check.length-1;i++){
//                                 buffer.append(check[i]+"/");}
//                             safeName = buffer.toString();}
                            
                        Container c;
                        if(Repository.container!=null)c = Repository.container.getParent();
                        else c = Repository.window;
                        new MySftpBrowser(Repository.c,tprescript,c);
//                         tprescript.setText(safeName);
                    
//                     }}
//                  catch(Exception e){
//                      fileChooser=null;
//                      e.printStackTrace();}
            }
        });

        browse2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent evt) {
                
//                 if(fileChooser==null)initializeFileBrowser();
//                 try{RETURN_TYPE answer = fileChooser.showOpenDialog(SuitaDetails.this);
//                     if (answer == RETURN_TYPE.APPROVE){
//                         FileObject aFileObject = fileChooser.getSelectedFile();
//                         String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
//                         safeName = safeName.substring(safeName.indexOf(Repository.host)+
//                                                         Repository.host.length());
//                         String [] check = safeName.split("/");
//                         if(check[check.length-1].equals(check[check.length-2])){
//                             StringBuffer buffer = new StringBuffer();
//                             for(int i=0;i<check.length-1;i++){
//                                 buffer.append(check[i]+"/");}
//                             safeName = buffer.toString();}
                        Container c;
                        if(Repository.container!=null)c = Repository.container.getParent();
                        else c = Repository.window;
                        new MySftpBrowser(Repository.c,tpostscript,c);
//                         tpostscript.setText(safeName);
//                     }}
//                  catch(Exception e){
//                      fileChooser=null;
//                      e.printStackTrace();}
            }
        });
        
        layout = new GroupLayout(global);
        global.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(stoponfail, javax.swing.GroupLayout.PREFERRED_SIZE, 105, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(savedb, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(40, 40, 40)
                .addComponent(tcdelay)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(ttcdelay, javax.swing.GroupLayout.DEFAULT_SIZE, 162, Short.MAX_VALUE)
                .addGap(65, 65, 65))
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
                    .addComponent(tprescript)
                    .addComponent(tpostscript))
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(browse1))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(browse2)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(13, 13, 13)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.CENTER)
                    .addComponent(stoponfail, javax.swing.GroupLayout.PREFERRED_SIZE, 20, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(savedb, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(tcdelay)
                    .addComponent(ttcdelay, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(13, 13, 13)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(prescript)
                    .addComponent(tprescript, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(browse1))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(tpostscript, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(browse2)
                    .addComponent(postscript))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {browse1, tprescript});

        layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {browse2, tpostscript});
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

//         layout = new GroupLayout(global);
//         global.setLayout(layout);
//         layout.setHorizontalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                     .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                         .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
//                             .addGap(5, 5, 5)
//                             .addComponent(prescript))
//                         .addComponent(stoponfail, GroupLayout.PREFERRED_SIZE, 120,
//                                      GroupLayout.PREFERRED_SIZE)
//                         .addComponent(savedb, GroupLayout.PREFERRED_SIZE, 120,
//                                      GroupLayout.PREFERRED_SIZE)
//                                      
//                                      )
//                     .addGroup(layout.createSequentialGroup()
//                         .addGap(5, 5, 5)
//                         .addComponent(postscript)))
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                     .addComponent(tprescript, GroupLayout.DEFAULT_SIZE, 216, Short.MAX_VALUE)
//                     .addComponent(tpostscript))
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                     .addComponent(browse1)
//                     .addComponent(browse2))
//                 .addGap(10, 10, 10)));
//                 
//         layout.setVerticalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
//                     .addComponent(stoponfail)
//                     .addComponent(savedb)
// //                     , GroupLayout.PREFERRED_SIZE, 
// //                                   GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
// //                     .addComponent(browse1)
//                     )
//                 
//                 
// //                 .addComponent(stoponfail)
//                 
// //                 .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                 
// //                 .addComponent(savedb)
// 
// 
// 
// 
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
//                     .addComponent(prescript)
//                     .addComponent(tprescript, GroupLayout.PREFERRED_SIZE, 
//                                   GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
//                     .addComponent(browse1))
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
//                     .addComponent(tpostscript, GroupLayout.PREFERRED_SIZE, 
//                                   GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
//                     .addComponent(browse2)
//                     .addComponent(postscript))
//                 .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)));
                
                
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
        defsContainer = new JPanel();
        setLayout(new BorderLayout());
        defsContainer.setBackground(new Color(255, 255, 255));
        defsContainer.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0));
        defsContainer.setLayout(new BoxLayout(defsContainer, BoxLayout.Y_AXIS));
        
        defsContainer.add(suiteoptions);
        
        scroll.setViewportView(global);
        add(scroll, BorderLayout.CENTER);
        JLabel l = new JLabel("test");            
        FontMetrics metrics = l.getFontMetrics(l.getFont());
        int width = 0;
        for(int i=0;i<descriptions.size();i++){
            if(width<metrics.stringWidth(descriptions.get(i)[Repository.LABEL])){
                width = metrics.stringWidth(descriptions.get(i)[Repository.LABEL]);
            }
        }
        for(int i=0;i<descriptions.size();i++){
            String button = descriptions.get(i)[Repository.SELECTED];
            DefPanel define = new DefPanel(descriptions.get(i)[Repository.LABEL],
                                                               button,
                                                               descriptions.get(i)[Repository.ID],
                                                               width,i,this);
            definitions.add(define);
            defsContainer.add(define);
        }
    }
    
    public void initSummary(){
        summary = new JPanel();
        summary.setBackground(Color.WHITE);
        summary.setPreferredSize(new Dimension(300,200));
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

        JLabel l7 = new JLabel("Stopped:");
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
//         
        JLabel l10 = new JLabel("Waiting:");
        l10.setBounds(10,175,60,25);
        summary.add(l10);
        stats[9] = new JLabel();
        stats[9].setBounds(118,175,100,25);

        for(JLabel l:stats){
            if(l!=null)summary.add(l);
        }
    }
    
    public void initTCOptions(){
        tcoptions = new JPanel();
        tcoptions.setBackground(Color.WHITE);
        JLabel tcname = new JLabel();
        ttcname = new JTextField();
        runnable = new JCheckBox();
        optional = new JCheckBox();
        prerequisites = new JCheckBox();

        tcname.setText("TC name:");

        runnable.setText("Runnable");

        optional.setText("Optional");

        prerequisites.setText("pre-requisites");

        GroupLayout layout = new GroupLayout(tcoptions);
        tcoptions.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(runnable)
                        .addGap(18, 18, 18)
                        .addComponent(optional)
                        .addGap(18, 18, 18)
                        .addComponent(prerequisites))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(tcname)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(ttcname, GroupLayout.PREFERRED_SIZE, 275, GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(127, Short.MAX_VALUE)));
                
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(tcname)
                    .addComponent(ttcname, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(runnable)
                    .addComponent(optional)
                    .addComponent(prerequisites))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)));
    }
           
    public int getDefsNr(){
        return definitions.size();}
        
    public ArrayList<DefPanel> getDefs(){
        return definitions;}
           
    public void clearDefs(){
        for(int i=0;i<definitions.size();i++){
            definitions.get(i).setDescription("");}}
            
    public void setParent(Item parent){ 
        this.parent = parent;
        if(parent!=null&&parent.getType()==2){
            try{String line = null;  
                InputStream in = Repository.c.get(Repository.REMOTEEPIDDIR);
                InputStreamReader inputStreamReader = new InputStreamReader(in);
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);  
                StringBuffer b=new StringBuffer("");
                while ((line=bufferedReader.readLine())!= null){b.append(line+";");}                        
                bufferedReader.close();
                inputStreamReader.close();
                in.close();
                String result = b.toString();
                String [] vecresult = result.split(";");                
                

                for(ListSelectionListener l:combo.getListSelectionListeners()){
                    combo.removeListSelectionListener(l);
                }

                combo.setModel(new DefaultComboBoxModel(vecresult));
                String [] strings = parent.getEpId();
                ArrayList<String> array = new ArrayList<String>(Arrays.asList(vecresult));
                int [] sel = new int[strings.length];
                for(int i=0;i<strings.length;i++){
                    sel[i]=array.indexOf(strings[i]);
                }
                combo.setSelectedIndices(sel);
                combo.addListSelectionListener(new MyListSelectionListener());
                

                
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
                        if(getItemParent().isVisible())Repository.window.mainpanel.p1.sc.g.updateLocations(getItemParent());
                        Repository.window.mainpanel.p1.sc.g.repaint();
                    }
                });
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
            ttcname.setText(getItemParent().getName());
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
                    if(getItemParent().isVisible())Repository.window.mainpanel.p1.sc.g.updateLocations(getItemParent());
                    Repository.window.mainpanel.p1.sc.g.repaint();
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
                    Repository.window.mainpanel.p1.sc.g.repaint();
                }
            });
            s = optional.getActionListeners();
            for(ActionListener a:s){
                optional.removeActionListener(a);
            }
            optional.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    if(optional.isSelected())getItemParent().setOptional(true);
                    else getItemParent().setOptional(false);
                    Repository.window.mainpanel.p1.sc.g.repaint();
                }
            });
            s = prerequisites.getActionListeners();
            for(ActionListener a:s){
                prerequisites.removeActionListener(a);
            }
            prerequisites.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    if(prerequisites.isSelected()){
                        Repository.window.mainpanel.p1.sc.g.setPreRequisites(getItemParent());
                    }
                    else{
                        getItemParent().setPrerequisite(false);
                        Repository.window.mainpanel.p1.sc.g.repaint();
                    }
                }
            });
            
        }
    }

    public void setSuiteDetails(boolean rootsuite){
        if(rootsuite){
            combo.setEnabled(true);
            ep.setEnabled(true);
            for(DefPanel p:definitions){
                defsContainer.add(p);
            }         
        } else {
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
        
    public boolean saveDB(){
        return savedb.isSelected();}
        
    public void setStopOnFail(boolean value){
        stoponfail.setSelected(value);}
        
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
//         container.setTitle(title);
    }
    
    public Item getItemParent(){
        return this.parent;
    }
        
        
//     public void initializeFileBrowser(){
//         fileChooser = new VFSJFileChooser("sftp://"+Repository.user+":"+
//                                            Repository.password+"@"+Repository.host+
//                                            "/home/"+Repository.user+"/twister/config/");        
//         fileChooser.setFileHidingEnabled(true);
//         fileChooser.setMultiSelectionEnabled(false);
//         fileChooser.setFileSelectionMode(VFSJFileChooser.SELECTION_MODE.FILES_AND_DIRECTORIES);}
    
    class MyListSelectionListener implements ListSelectionListener {
        public void valueChanged(ListSelectionEvent evt) {
            if (!evt.getValueIsAdjusting()) {
                JList list = (JList)evt.getSource();
                String [] selected = new String[list.getSelectedValuesList().size()];
                for(int i=0;i<list.getSelectedValuesList().size();i++){
                    selected[i] = list.getSelectedValuesList().get(i).toString();
                }
                getItemParent().setEpId(selected);
                Repository.window.mainpanel.p1.sc.g.repaint();
            }
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
        userDefinition.setText("");
        userDefinition.setMaximumSize(new Dimension(300, 100));
        userDefinition.setMinimumSize(new Dimension(50, 20));
        userDefinition.setPreferredSize(new Dimension(100, 20));
        add(userDefinition);
        userDefinition.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(parent!=null){
                    System.out.println(parent.getName()+" "+userDefinition.getText());
                    setParentField(userDefinition.getText(),false);}}});
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
                    if(Repository.container!=null)c = Repository.container.getParent();
                    else c = Repository.window;
                    new MySftpBrowser(Repository.c,userDefinition,c);
                    if(parent!=null){
                        setParentField(userDefinition.getText(),false);}
                    }
                    
                });
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
                            String result = Repository.getRPCClient().execute("runUserScript",
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
    
    public void setDescription(String desc){
        userDefinition.setText(desc);}}      