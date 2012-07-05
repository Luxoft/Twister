/*
File: applet.java ; This file is part of Twister.

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
import net.sf.vfsjfilechooser.VFSJFileChooser;
import net.sf.vfsjfilechooser.VFSJFileChooser.RETURN_TYPE;
import org.apache.commons.vfs.FileObject;
import net.sf.vfsjfilechooser.utils.VFSUtils;

public class SuitaDetails extends JPanel {
    private JPanel defsContainer;
    private JScrollPane scroll;
    private ArrayList <DefPanel> definitions = new ArrayList <DefPanel>();
    private TitledBorder border;    
    
    public void setEnabled(boolean enabled) {
        super.setEnabled(enabled);
        for (Component component : definitions)
            component.setEnabled(enabled);}
    
    public SuitaDetails(ArrayList<String []> descriptions) {
        initComponents(descriptions);}
        
    public void setTitle(String title){
        border.setTitle(title);
        repaint();}
        
    public void restart(ArrayList<String []> descriptions){
        removeAll();
        initComponents(descriptions);
        repaint();}
        
    private void initComponents(ArrayList<String []> descriptions){
        definitions.clear();
        border = BorderFactory.createTitledBorder("No suite");
        setBorder(border);
        scroll = new JScrollPane();
        defsContainer = new JPanel();
        setLayout(new BorderLayout());
        defsContainer.setBackground(new Color(255, 255, 255));
        defsContainer.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0));
        defsContainer.setLayout(new BoxLayout(defsContainer, BoxLayout.Y_AXIS));
        scroll.setViewportView(defsContainer);
        add(scroll, java.awt.BorderLayout.CENTER);
        JLabel l = new JLabel("test");            
        FontMetrics metrics = l.getFontMetrics(l.getFont());
        int width = 0;
        for(int i=0;i<descriptions.size();i++){
            if(width<metrics.stringWidth(descriptions.get(i)[Repository.LABEL])){
                width = metrics.stringWidth(descriptions.get(i)[Repository.LABEL]);}}
        for(int i=0;i<descriptions.size();i++){
            String button = descriptions.get(i)[Repository.SELECTED];
            DefPanel define = new DefPanel(descriptions.get(i)[Repository.LABEL],button,descriptions.get(i)[Repository.ID],width,i,this);
            definitions.add(define);
            defsContainer.add(define);}
        setEnabled(false);}
           
    public int getDefsNr(){
        return definitions.size();}
        
    public ArrayList<DefPanel> getDefs(){
        return definitions;}
           
    public void clearDefs(){
        for(int i=0;i<definitions.size();i++){
            definitions.get(i).setDecription("");}}
            
    public void setParent(Item parent){ 
        for(int i=0;i<definitions.size();i++){
            definitions.get(i).setParent(parent);}}
            
    public DefPanel getDefPanel(int i){
        return definitions.get(i);}}
        
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
    
    public DefPanel(String descriptions,String button,String id, int width,final int index, SuitaDetails container){
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
        filedsGapLayout.setHorizontalGroup(filedsGapLayout.createParallelGroup(GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
        filedsGapLayout.setVerticalGroup(filedsGapLayout.createParallelGroup(GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
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
                    setParentField(userDefinition.getText(),false);}}});
        filedsGap = new JPanel();
        filedsGap.setBackground(new Color(255, 255, 255));
        filedsGap.setMaximumSize(new Dimension(20, 20));
        filedsGap.setMinimumSize(new Dimension(20, 20));
        filedsGap.setPreferredSize(new Dimension(20, 20));
        filedsGapLayout = new GroupLayout(filedsGap);
        filedsGap.setLayout(filedsGapLayout);
        filedsGapLayout.setHorizontalGroup(filedsGapLayout.createParallelGroup(GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
        filedsGapLayout.setVerticalGroup(filedsGapLayout.createParallelGroup(GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
        add(filedsGap);      
        filedsGap = new JPanel();
        filedsGap.setBackground(new Color(255, 255, 255));
        filedsGap.setMaximumSize(new Dimension(20, 20));
        filedsGap.setMinimumSize(new Dimension(20, 20));
        filedsGap.setPreferredSize(new Dimension(20, 20));
        filedsGapLayout = new GroupLayout(filedsGap);
        filedsGap.setLayout(filedsGapLayout);
        filedsGapLayout.setHorizontalGroup(filedsGapLayout.createParallelGroup(GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
        filedsGapLayout.setVerticalGroup(filedsGapLayout.createParallelGroup(GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
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
                    frame.setLocation((int)database.getLocationOnScreen().getX()-100,(int)database.getLocationOnScreen().getY());
                    frame.setVisible(true);}});}
//         else if(button.equals("UserScript")){
//             JButton script = new JButton("Script");
//             script.setMaximumSize(new Dimension(100, 20));
//             script.setMinimumSize(new Dimension(50, 20));
//             script.setPreferredSize(new Dimension(80, 20));
//             add(script);
//             script.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     
//                     VFSJFileChooser fileChooser = Repository.window.mainpanel.p4.getConfig().getChooser();
//                     try{RETURN_TYPE answer = fileChooser.showOpenDialog(DefPanel.this);
//                         if (answer == RETURN_TYPE.APPROVE){
//                             FileObject aFileObject = fileChooser.getSelectedFile();
//                             String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
//                             safeName = safeName.substring(safeName.indexOf(Repository.host)+
//                                                             Repository.host.length());
//                             String [] check = safeName.split("/");
//                             if(check[check.length-1].equals(check[check.length-2])){
//                                 StringBuffer buffer = new StringBuffer();
//                                 for(int i=0;i<check.length-1;i++){
//                                     buffer.append(check[i]+"/");}
//                                 safeName = buffer.toString();}
//                             
//                         }}
//                     catch(Exception e){
//                         e.printStackTrace();
//                     }
//                     
//                     
//                     
//                     
//                     
//                 }});
//                 
//             filedsGap = new JPanel();
//             filedsGap.setBackground(new Color(255, 255, 255));
//             filedsGap.setMaximumSize(new Dimension(10, 10));
//             filedsGap.setMinimumSize(new Dimension(10, 10));
//             filedsGap.setPreferredSize(new Dimension(10, 10));    
//             filedsGapLayout = new GroupLayout(filedsGap);
//             filedsGap.setLayout(filedsGapLayout);
//             filedsGapLayout.setHorizontalGroup(filedsGapLayout.createParallelGroup(GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
//             filedsGapLayout.setVerticalGroup(filedsGapLayout.createParallelGroup(GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
//             filedsGap.setLayout(filedsGapLayout);           
//             add(filedsGap); 
//             
//             JButton value = new JButton("Value");
//             value.setMaximumSize(new Dimension(100, 20));
//             value.setMinimumSize(new Dimension(50, 20));
//             value.setPreferredSize(new Dimension(80, 20));
//             add(value);
//             value.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     
//                     
//                 }});
//             }
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
            container.setTitle("Suite "+
                                parent.getName());
            container.setEnabled(true);}
        else{
            container.setEnabled(false);
            container.setTitle("No suite");}
        this.parent = parent;}
        
    public String getDescription(){
        return descriptions;}
    
    public void setDecription(String desc){
        userDefinition.setText(desc);}}