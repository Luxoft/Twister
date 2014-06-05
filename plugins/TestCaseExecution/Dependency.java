/*
File: Dependency.java ; This file is part of Twister.
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
import javax.swing.JPanel;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import com.twister.Item;
import com.twister.CustomDialog;
import java.util.ArrayList;
import javax.swing.JList;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JScrollPane;
import javax.swing.JDialog;
import javax.swing.JButton;
import javax.swing.JOptionPane;
import java.util.HashMap;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.Color;
import java.awt.BorderLayout;
import javax.swing.BorderFactory;

public class Dependency extends JPanel{
    private javax.swing.JButton add;
    private javax.swing.JLabel dtc;
    private javax.swing.JComboBox dvalue;
    private javax.swing.JPanel jPanel3;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JButton remove;
    private Item parent;
    
    public Dependency(){
        initComponents();
    }
    
    private void initComponents() {
        JPanel background = new JPanel();
        setLayout(new BorderLayout());
        background.setBackground(Color.WHITE);
        add(background,BorderLayout.CENTER);
        add = new javax.swing.JButton();
        jScrollPane1 = new javax.swing.JScrollPane();
        jPanel3 = new javax.swing.JPanel();
        jPanel3.setBackground(Color.WHITE);
        add.setText("Add");
        jPanel3.setLayout(new javax.swing.BoxLayout(jPanel3, javax.swing.BoxLayout.PAGE_AXIS));
        jScrollPane1.setViewportView(jPanel3);
        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(background);
        background.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(0, 428, Short.MAX_VALUE)
                        .addComponent(add, javax.swing.GroupLayout.PREFERRED_SIZE, 82, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(jScrollPane1))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 402, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(add)
                .addContainerGap())
        );
        Item i = null;
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(parent==null)return;
                //start building tc's array
                ArrayList <TCsListElement> tcs = new ArrayList();
                StringBuilder path = new StringBuilder();
                for(Item i:RunnerRepository.getSuite()){
                    if(i==parent)continue;
                    if(i.getType()==1){
                        tcs.add(new TCsListElement(i,""));
                    } else {
                        path.setLength(0);
                        addTCs(i,tcs,path,parent);
                    }
                }
                tcs = getSelectedElement(tcs);//elements to add as dependencie
                //add selected elems(dependencie) as InstancePanel in GUI and in parent dependencie
                for(TCsListElement elem:tcs){
                    jPanel3.add(new InstancePanel(Dependency.this,elem.getParent(),elem.toString(),"Pass"));
                    parent.getDependencies().put(elem.getParent(), "Pass");
                }
                jPanel3.revalidate();
                RunnerRepository.window.mainpanel.p1.sc.g.repaint();
            }
        });
    }
    
    private ArrayList <TCsListElement> getSelectedElement(ArrayList <TCsListElement> tcs){
        TCsListElement [] elems = new TCsListElement[tcs.size()];
        for(int i=0;i<tcs.size();i++){
            elems[i] = tcs.get(i);
        }
        JScrollPane jScrollPane1 = new JScrollPane();
        final JList <TCsListElement> jList1 = new JList();
        jList1.setModel(new DefaultComboBoxModel(elems));
        JPanel libraries = new JPanel();
        libraries.setLayout(new java.awt.BorderLayout());
        jScrollPane1.setViewportView(jList1);
        libraries.add(jScrollPane1,java.awt.BorderLayout.CENTER);
        libraries.setBackground(java.awt.Color.RED);
        JButton ok = new JButton("OK");
        JButton cancel = new JButton("Cancel");
        final JDialog dialog = CustomDialog.getDialog(libraries, new JButton[]{ok,cancel},
                                                    JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION,
                                                    RunnerRepository.window,
                                                    "Please select TC's", null);
        dialog.setResizable(true);
        dialog.setSize(400, 600);
        dialog.addWindowListener(new WindowAdapter(){
        public void windowClosing(WindowEvent e){
            jList1.clearSelection();
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
              jList1.clearSelection();
              dialog.setVisible(false);
              dialog.dispose();
          }
        });
        dialog.setVisible(true); 
        tcs.clear();
        for(Object ob:jList1.getSelectedValuesList()){
            tcs.add((TCsListElement)ob);
        }
        return tcs;
    }
    
    /*
     * add tc's to tc's array
     */
    private void  addTCs(Item i,ArrayList <TCsListElement> tc,StringBuilder path,Item omit){
        if(i==omit)return;
        if(i.getType()==1){
            tc.add(new TCsListElement(i,path.toString()));
        } else if(i.getType()==2){
            path.append(i.getName()+"/");
            for(Item subitem:i.getSubItems()){
                addTCs(subitem,tc,new StringBuilder(path.toString()),omit);
            }
        }
    }
        
    public void removeDependencie(InstancePanel dependencie){
        jPanel3.remove(dependencie);
        jPanel3.revalidate();
        jPanel3.repaint();
    }
    
    /*
     * setter method for parent to
     * setup dependencie editing panel in GUI,
     * handeled by suitadetails class setParent.
     */
    public void setParent(Item parent){
        this.parent = parent;
        jPanel3.removeAll();
        
        if(parent==null){
            add.setEnabled(false);
        } else {
            add.setEnabled(true);
            //start interpret parent dependencie and add them to GUI
            HashMap<Item,String> dependencies = parent.getDependencies();
            if(dependencies.size()>0){
                Item [] items = new Item[dependencies.keySet().size()];
                dependencies.keySet().toArray(items);
                StringBuilder path = new StringBuilder(); 
                ArrayList <TCsListElement> tcs = new ArrayList();
                for(Item i:items){
                    if(i==null){
                        System.out.println("ERROR! "+parent.getFileLocation()+" has invalid dependencies in project");
                        continue;
                    }
                    if(!Grafic.chekItemInArray(i, false)){
                        System.out.println("ERROR! Dependency item: "+i.getFileLocation()+" was deleted from project!");
                        continue;
                    }
                    path.setLength(0);
                    Item iparent = Grafic.getFirstSuitaParent(i, false);//build path of upper parents
                    while(iparent!=null){
                        path = path.insert(0,iparent.getName()+"/");//must inverse parents order for path
                        iparent = Grafic.getFirstSuitaParent(iparent, false);
                    }
                    if(i.getType()==1){
                        tcs.add(new TCsListElement(i,path.toString()));
                    } else {
                        addTCs(i,tcs,path,null);
                    }
                }
                for(TCsListElement elem:tcs){
                    jPanel3.add(new InstancePanel(Dependency.this,elem.getParent(),elem.toString(),dependencies.get(elem.getParent())));
                }
            }
        }
        jPanel3.revalidate();
        jPanel3.repaint();
    }
    
    /*
     * getter method for the parent item
     */
    public Item getDependencieParent(){
        return parent;
    }
    
    
    class InstancePanel extends JPanel{
        private Dependency parent;//this panel parent container
        private Item dependencie;
        
        public InstancePanel(final Dependency parent,final Item dependencie,String path,String value){
            this.dependencie = dependencie;
            this.parent = parent;
            setBackground(Color.WHITE);
            javax.swing.JLabel dtc = new javax.swing.JLabel(path);
            dtc.setMaximumSize(new java.awt.Dimension(300, 14));
            dtc.setMinimumSize(new java.awt.Dimension(30, 14));
            dtc.setPreferredSize(new java.awt.Dimension(30, 14));
            javax.swing.JComboBox dvalue = new javax.swing.JComboBox();
            dvalue.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Pass", "Fail" , "Any"}));
            if(value.equals("Pass"))dvalue.setSelectedIndex(0);
            else if (value.equals("Fail"))dvalue.setSelectedIndex(1);
            else dvalue.setSelectedIndex(2);
            dvalue.addItemListener(new ItemListener(){
                public void itemStateChanged(ItemEvent e){
                    if(e.getStateChange()==ItemEvent.SELECTED){
                        if(e.getItem().toString().equals("Pass")){
                            parent.getDependencieParent().getDependencies().put(dependencie, "Pass");
                        } else if(e.getItem().toString().equals("Fail")){
                            parent.getDependencieParent().getDependencies().put(dependencie, "Fail");
                        } else {
                            parent.getDependencieParent().getDependencies().put(dependencie, "Any");
                        }
                    }
                }
            });
            javax.swing.JButton remove = new javax.swing.JButton("Remove");
            setMaximumSize(new java.awt.Dimension(30000, 40));
            setMinimumSize(new java.awt.Dimension(30, 40));
            setPreferredSize(new java.awt.Dimension(30, 40));
            javax.swing.GroupLayout InstancePanelLayout = new javax.swing.GroupLayout(this);
            this.setLayout(InstancePanelLayout);
            InstancePanelLayout.setHorizontalGroup(
                InstancePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(InstancePanelLayout.createSequentialGroup()
                    .addContainerGap()
                    .addComponent(dtc, javax.swing.GroupLayout.DEFAULT_SIZE, 325, Short.MAX_VALUE)
                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                    .addComponent(dvalue, javax.swing.GroupLayout.PREFERRED_SIZE, 72, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                    .addComponent(remove)
                    .addContainerGap())
            );
            InstancePanelLayout.setVerticalGroup(
                InstancePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(InstancePanelLayout.createSequentialGroup()
                    .addContainerGap()
                    .addGroup(InstancePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(dtc, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(dvalue, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(remove))
                    .addContainerGap(6, Short.MAX_VALUE))
            );
            InstancePanelLayout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {dtc, dvalue, remove});
            remove.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    parent.removeDependencie(InstancePanel.this);
                    parent.parent.getDependencies().remove(dependencie);
                    RunnerRepository.window.mainpanel.p1.sc.g.repaint();
                }
            });
        }
    }
    
    class TCsListElement {
        private Item parent;
        private String path;//path to parent tc in project
        
        public TCsListElement(Item parent,String path){
            this.parent = parent;
            this.path = path;
        }
        
        public String toString(){
            return path+parent.getFileLocation().substring(1);
        }
        
        public Item getParent(){
            return parent;
        }
    }
    
}