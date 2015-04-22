/*
File: TestConfigManagement.java ; This file is part of Twister.
Version: 3.004

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

import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import java.awt.Dimension;
import javax.swing.DefaultComboBoxModel;
import javax.swing.table.DefaultTableModel;
import com.twister.CustomDialog;
import com.twister.Item;
import com.twister.Configuration;
import java.util.Collections;
import java.util.ArrayList;
import java.util.Arrays;
import java.awt.Color;
import java.awt.BorderLayout;
import javax.swing.JComboBox;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;

public class TestConfigManagement extends JPanel{
    
    private javax.swing.JButton add;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPanel jPanel4;
    private javax.swing.JPanel jPanel6;
    private javax.swing.JScrollPane jScrollPane2;
    private TestConfigTable jTable1;
    private javax.swing.JButton movebottom;
    private javax.swing.JButton movedown;
    private javax.swing.JButton movetop;
    private javax.swing.JButton moveup;
    private javax.swing.JButton remove;
    private javax.swing.JButton removeall;
    private Item parent;
    private JLabel iteratornr;
    private JComboBox saveconfig;
    
    public TestConfigManagement(){
        initComponents();
    }
    
    private void initComponents() {

        jPanel1 = new javax.swing.JPanel();
        add = new javax.swing.JButton();
        remove = new javax.swing.JButton();
        removeall = new javax.swing.JButton();
        movetop = new javax.swing.JButton();
        moveup = new javax.swing.JButton();
        movedown = new javax.swing.JButton();
        movebottom = new javax.swing.JButton();
        jPanel2 = new javax.swing.JPanel();
        jPanel4 = new javax.swing.JPanel();
        jPanel6 = new javax.swing.JPanel();
        jScrollPane2 = new javax.swing.JScrollPane();
        jTable1 = new TestConfigTable(this);

        add.setText("Add");
        add.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addConfig();
            }
        });

        remove.setText("Remove");
        remove.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                removeConfig();
            }
        });

        removeall.setText("Remove All");
        removeall.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                if(parent==null)return;
                ((DefaultTableModel)jTable1.getModel()).setRowCount(0);
                parent.getConfigurations().clear();
                if(parent.getType()==2){
                    updatedSuiteConfig(true,parent,parent.getConfigurations());
                }
                RunnerRepository.window.mainpanel.p1.sc.g.repaint();
                updateIteratorNr();
            }
        });

        movetop.setText("Move to Top");
        movetop.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                moveTop();
            }
        });
        

        moveup.setText("Move Up");
        moveup.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                moveUp();
            }
        });

        movedown.setText("Move Down");
        movedown.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                moveDown();
            }
        });

        movebottom.setText("Move to Bottom");
        movebottom.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                moveBottom();
            }
        });

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addGap(0, 34, Short.MAX_VALUE)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(movebottom)
                    .addComponent(movedown)
                    .addComponent(moveup)
                    .addComponent(movetop)
                    .addComponent(removeall)
                    .addComponent(remove)
                    .addComponent(add))
                .addGap(30, 30, 30))
        );

        jPanel1Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {add, movebottom, movedown, movetop, moveup, remove, removeall});

        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addComponent(add)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(remove)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(removeall)
                .addGap(18, 18, 18)
                .addComponent(movetop)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(moveup)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(movedown)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(movebottom))
        );

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        
        JPanel iteratorpanel = new JPanel();
        iteratorpanel.setLayout(new BorderLayout());
        iteratorpanel.setMinimumSize(new Dimension(150,40));
        iteratorpanel.setPreferredSize(new Dimension(150,40));
        JLabel saveconfigslabel = new JLabel("Save iterations: ");
        saveconfig = new JComboBox();
        saveconfig.addItemListener(new ItemListener(){
            @Override
            public void itemStateChanged(ItemEvent e){
               if(e.getStateChange() == ItemEvent.SELECTED){
                   if(parent!=null&&parent.getType()==1){
                       parent.setSaveconfig(saveconfig.getSelectedItem().toString());
                    }
        }}});
        JPanel saveconfigpanel = new JPanel();
        saveconfigpanel.add(saveconfigslabel);
        saveconfigpanel.add(saveconfig);
        
        
        saveconfig.setModel(new DefaultComboBoxModel(new String[] {"all","failed"}));
        
        iteratornr = new JLabel("Total iterators: ");
        iteratornr.setFont(iteratornr.getFont().deriveFont(15.0f));
        
        iteratorpanel.add(saveconfigpanel,BorderLayout.WEST);
        JPanel temp = new JPanel();
        temp.add(iteratornr);
        iteratorpanel.add(temp,BorderLayout.CENTER);
        JPanel tablepanel = new JPanel();
        tablepanel.setLayout(new BorderLayout());
        tablepanel.add(jScrollPane2,BorderLayout.CENTER);
        tablepanel.add(iteratorpanel,BorderLayout.NORTH);
        
        jScrollPane2.setViewportView(jTable1);
        javax.swing.GroupLayout jPanel6Layout = new javax.swing.GroupLayout(jPanel6);
        jPanel6.setLayout(jPanel6Layout);
        jPanel6Layout.setHorizontalGroup(
            jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel6Layout.createSequentialGroup()
                //.addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 774, Short.MAX_VALUE)
                .addComponent(tablepanel, javax.swing.GroupLayout.DEFAULT_SIZE, 774, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addComponent(jPanel2, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(0, 0, 0))
        );
        jPanel6Layout.setVerticalGroup(
            jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(tablepanel, javax.swing.GroupLayout.DEFAULT_SIZE, 443, Short.MAX_VALUE)
            .addGroup(jPanel6Layout.createSequentialGroup()
                .addComponent(jPanel4, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel2, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(jPanel6, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel6, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );
    }
    
    public void updateIteratorNr(){
        if(parent==null || parent.getType()==2){
            iteratornr.setText("Total iterators: 0");
            return;}
        StringBuilder sb = new StringBuilder();
        for(Configuration conf:parent.getConfigurations()){
            if(!conf.isEnabled())continue;
            sb.append(conf.getFile());
            sb.append(",");
            sb.append(conf.isIeratorOD());
            sb.append(";");
        }
        
        try{String respons = RunnerRepository.getRPCClient().execute("get_iterations", new Object[]{RunnerRepository.user,sb.toString()}).toString();
            if(respons.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, 
                                      TestConfigManagement.this, "ERROR", 
                                      respons);
            } else {
                iteratornr.setText("Total iterators: "+Integer.parseInt(respons));
            }
        } catch(Exception e){
            System.out.println("There was an error in updating iterators numbers!!!");
            e.printStackTrace();
        }
    }
    
    public void configModified(String filename,boolean enabled, boolean iteratorod, boolean iteratorsof){
        for(Configuration conf:parent.getConfigurations()){
            if(conf.getFile().equals(filename)){
                conf.setEnabled(enabled);
                conf.setIeratorOD(iteratorod);
                conf.setIteratorSOF(iteratorsof);
                break;
            }
        }
        if(parent.getType()==2){
            updatedSuiteConfig(true,parent,parent.getConfigurations());
        }
        updateIteratorNr();
    }
    
    
    //update all subchildren with the modified config array
    public void updatedSuiteConfig(boolean skip, Item item, ArrayList<Configuration>configs){
        ArrayList<Configuration>clones = new ArrayList<Configuration>();
        for(Configuration conf:configs){
            Configuration clone = conf.clone();
            clone.setFromSuite(true);
            clones.add(clone);
        }
        
        if(item.getType()==1){//if item is tc do the magic
            
            //remove all configs from suite
            ArrayList<Configuration>toremove=new ArrayList<Configuration>();
            for(Configuration cfg:item.getConfigurations()){
                if(cfg.isFromSuite())toremove.add(cfg);
            }
            for(Configuration cfg:toremove){
                item.getConfigurations().remove(cfg);
            }
            
            //get duplicated configs for future removal
            toremove.clear();
            for(Configuration cfg:clones){
                for(Configuration itemcfg:item.getConfigurations()){
                    if(itemcfg.getFile().equals(cfg.getFile())){
                        toremove.add(cfg);
                        break;
                    }
                }
            }
            
            //install the configs
            item.getConfigurations().addAll(0, clones);
            
            //remove the existing ones
            for(Configuration conf:toremove){
                item.getConfigurations().remove(conf);
            }
            
        } else if(item.getType()==2){//if item is suite update his children and do the magic on it to
            if(!skip){//used to skip on first iteration
                item.getConfigurations().clear();
                item.getConfigurations().addAll(0, clones);    
            }
            for(Item i:item.getSubItems()){
                updatedSuiteConfig(false,i,configs);
            }
        }
    }
    
    //move selected row to bottom
    public void moveBottom(){
        if(parent==null||jTable1.getSelectedRows().length==0)return;
        DefaultTableModel tm = (DefaultTableModel) jTable1.getModel();
        int[] rows = jTable1.getSelectedRows();
        int reverserows [] = new int [rows.length];
        for(int i=rows.length-1;i>-1;i--){
            reverserows[rows.length-i-1] = rows[i];
        }
        int move = tm.getRowCount()-rows[rows.length-1]-1;
        jTable1.clearSelection();
        for (int row : reverserows){
            //tm.moveRow(row, row, jTable1.getRowCount()-1);
            tm.moveRow(row, row, row+move);
            jTable1.addRowSelectionInterval(row+move,row+move);
            Configuration tomove = parent.getConfigurations().get(row);
            parent.getConfigurations().remove(tomove);
            parent.getConfigurations().add(row+move,tomove);
        }
        if(parent.getType()==2){
            updatedSuiteConfig(true,parent,parent.getConfigurations());
        }
        RunnerRepository.window.mainpanel.p1.sc.g.repaint();
    }
    
    //move selected row to top
    public void moveTop(){
        if(parent==null||jTable1.getSelectedRows().length==0)return;
        DefaultTableModel tm = (DefaultTableModel) jTable1.getModel();
        int[] rows = jTable1.getSelectedRows();
        
        int move = rows[0];
        jTable1.clearSelection();
        for (int row : rows){
            tm.moveRow(row, row, row-move);
            jTable1.addRowSelectionInterval(row-move,row-move);
            Configuration tomove = parent.getConfigurations().get(row);
            parent.getConfigurations().remove(tomove);
            parent.getConfigurations().add(row-move,tomove);    
        }
        if(parent.getType()==2){
            updatedSuiteConfig(true,parent,parent.getConfigurations());
        }
        RunnerRepository.window.mainpanel.p1.sc.g.repaint();
    }
    
    //move selected row one row down
    public void moveDown(){
        if(parent==null)return;
        DefaultTableModel tm = (DefaultTableModel) jTable1.getModel();
        int[] rows = jTable1.getSelectedRows();
        int reverserows [] = new int [rows.length];
        for(int i=rows.length-1;i>-1;i--){
            reverserows[rows.length-i-1] = rows[i];
        }
        jTable1.clearSelection();
        for (int row : reverserows) {
            if(row<jTable1.getRowCount()-1){
                tm.moveRow(row, row, row+1);
                jTable1.addRowSelectionInterval(row+1,row+1);
                Collections.swap(parent.getConfigurations(),row,row+1);
            }
        }
        if(parent.getType()==2){
            updatedSuiteConfig(true,parent,parent.getConfigurations());
        }
        RunnerRepository.window.mainpanel.p1.sc.g.repaint();
    }
    
    //move selected row one row up
    public void moveUp(){
        if(parent==null)return;
        DefaultTableModel tm = (DefaultTableModel) jTable1.getModel();
        int[] rows = jTable1.getSelectedRows();
        jTable1.clearSelection();
        for (int row : rows) {
            if(row>0){
                tm.moveRow(row, row, row-1);
                Collections.swap(parent.getConfigurations(),row,row-1);
                jTable1.addRowSelectionInterval(row-1,row-1);
            }
        }
        if(parent.getType()==2){
            updatedSuiteConfig(true,parent,parent.getConfigurations());
        }
        RunnerRepository.window.mainpanel.p1.sc.g.repaint();
    }
    
    //remove selected configs from parent
    public void removeConfig(){
        if(parent==null)return;
        int[] rows = jTable1.getSelectedRows();
        int reverserows [] = new int [rows.length];
        for(int i=rows.length-1;i>-1;i--){
            reverserows[rows.length-i-1] = rows[i];
        }
        DefaultTableModel tm = (DefaultTableModel) jTable1.getModel();
        for (int row : reverserows) {
            String filename = tm.getValueAt(row, 0).toString();
            for(Configuration conf:parent.getConfigurations()){
                if(conf.getFile().equals(filename)){
                    parent.getConfigurations().remove(conf);
                    break;
                }
            }
            tm.removeRow(jTable1.convertRowIndexToModel(row));
        }
        jTable1.clearSelection();
        if(parent.getType()==2){
            updatedSuiteConfig(true,parent,parent.getConfigurations());
        }
        RunnerRepository.window.mainpanel.p1.sc.g.repaint();
        updateIteratorNr();
    }
    
    public void addConfig(){
        if(parent==null)return;
        JPanel p = new JPanel();
        p.setLayout(null);
        p.setPreferredSize(new Dimension(515,200));
        JLabel ep = new JLabel("Configurations: ");
        ep.setBounds(5,5,95,25);
        JList tep = new JList();
        JScrollPane scep = new JScrollPane(tep);
        scep.setBounds(100,5,400,180);
        p.add(ep);
        p.add(scep);
        String [] vecresult = RunnerRepository.window.mainpanel.p4.getTestConfig().tree.getFiles();
        
        ArrayList<String> array = new ArrayList<String>(Arrays.asList(vecresult));
        ArrayList<String> torem = new ArrayList<String>();
        for(int i=0;i<vecresult.length;i++){
            for(Configuration conf:parent.getConfigurations()){
                if(conf.getFile().equals(vecresult[i])){
                    torem.add(vecresult[i]);
                    break;
                }
            }
        }
        for(String s:torem){
            array.remove(s);
        }
        Object [] resultingarray = array.toArray();
        tep.setModel(new DefaultComboBoxModel(resultingarray));
        
        
        
        
        //tep.setModel(new DefaultComboBoxModel(vecresult));
        int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                            JOptionPane.OK_CANCEL_OPTION, TestConfigManagement.this, "Test Configurations Files",null);
        if(resp == JOptionPane.OK_OPTION){
            String configs[] = new String[tep.getSelectedValuesList().size()];
            DefaultTableModel dtm = (DefaultTableModel)jTable1.getModel();
            String name;
            boolean goon;
            for(int i=0;i<configs.length;i++){
                goon = true;
                name = tep.getSelectedValuesList().get(i).toString();
                for(Configuration conf:parent.getConfigurations()){
                    if(conf.getFile().equals(name)){
                        goon = false;
                        break;
                    }
                }
                if(!goon)continue;
                dtm.addRow(new Object[]{name,new Boolean(true),new Boolean(false),new Boolean(false)});
                Configuration conf = new Configuration(name);
                conf.setEnabled(true);
                conf.setIeratorOD(false);
                conf.setIteratorSOF(false);
                if(parent.getType()==2)conf.setFromSuite(true);
                parent.getConfigurations().add(conf);
            }
            if(parent.getType()==2){
                updatedSuiteConfig(true,parent,parent.getConfigurations());
            }
            RunnerRepository.window.mainpanel.p1.sc.g.repaint();
        }
        updateIteratorNr();
    }
    
    public void setParent(Item parent){
        this.parent = parent;
        DefaultTableModel model =(DefaultTableModel)jTable1.getModel();
        model.setRowCount(0);
        if(parent!=null){
            if(RunnerRepository.window.mainpanel.p1.getOptionsTabs().getComponentZOrder(this)==-1){
                RunnerRepository.window.mainpanel.p1.getOptionsTabs().addTab("Test Configurations", this);
            }
            for(Configuration conf:parent.getConfigurations()){
                model.addRow(new Object[]{conf.getFile(),new Boolean(conf.isEnabled()),new Boolean(conf.isIeratorOD()),new Boolean(conf.isIteratorSOF())});
            }
        } else {
            if(RunnerRepository.window.mainpanel.p1.getOptionsTabs().getComponentZOrder(this)!=-1){
                RunnerRepository.window.mainpanel.p1.getOptionsTabs().remove(this);
            }
        }
        updateIteratorNr();
        if(parent!=null){
            String itemsaveconfig = parent.getSaveconfig();
            int size = saveconfig.getItemCount();
            for(int i=0;i<size;i++){
                if(saveconfig.getItemAt(i).toString().equals(itemsaveconfig)){
                    saveconfig.setSelectedIndex(i);
                    break;
                }
            }
        }
    }
    
    public Item getConfigParent(){
        return this.parent;
    }

}
