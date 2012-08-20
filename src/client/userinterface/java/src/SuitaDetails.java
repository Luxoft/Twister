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
import javax.swing.JFrame;
import javax.swing.JCheckBox;
import javax.swing.LayoutStyle;
import javax.swing.border.TitledBorder;
import javax.swing.JComboBox;

public class SuitaDetails extends JPanel {
    private JPanel defsContainer,global, suiteoptions;
    private JScrollPane scroll;
    private ArrayList <DefPanel> definitions = new ArrayList <DefPanel>();
    private TitledBorder border;    
    private JCheckBox stoponfail;
    private JTextField tprescript, tpostscript;
    private JButton browse1,browse2;
    private VFSJFileChooser fileChooser;
    
    
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
        
    private void initGlobal(){
        suiteoptions = new JPanel();
//         JLabel ep = new JLabel("EP:");
//         JLabel name = new JLabel("Suite name:");
//         JTextField tname = new JTextField();
//         JComboBox combo = new JComboBox();
//         suiteoptions.add(ep);
//         suiteoptions.add(combo);
        
        
        
        
        JLabel suitename = new JLabel();
        JTextField tsuitename = new JTextField();
        JPanel jPanel1 = new JPanel();
        JLabel ep = new JLabel();
        JComboBox combo = new JComboBox();

        suiteoptions.setBackground(Color.WHITE);

        suitename.setBackground(Color.WHITE);
        suitename.setText("Suite name: ");
        suiteoptions.add(suitename);

        tsuitename.setPreferredSize(new Dimension(150, 20));
        suiteoptions.add(tsuitename);

        jPanel1.setBackground(Color.WHITE);
        jPanel1.setMinimumSize(new Dimension(0, 0));
        jPanel1.setPreferredSize(new Dimension(20, 20));

        

        suiteoptions.add(jPanel1);

        ep.setText("EP: ");
        suiteoptions.add(ep);

        //combo.setModel(new DefaultComboBoxModel(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));
        combo.setPreferredSize(new java.awt.Dimension(100, 20));
        suiteoptions.add(combo);
        
        
        
        
        
        
        
        
        
        
        
        
        
        stoponfail = new JCheckBox();
        JLabel prescript = new JLabel();
        JLabel postscript = new JLabel();
        tprescript = new JTextField();
        tpostscript = new JTextField();
        browse1 = new JButton("...");
        browse2 = new JButton("...");

        stoponfail.setText("Stop on fail");
        prescript.setText("Pre execution script:");
        postscript.setText("Post execution script:");
        
        browse1.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                if(fileChooser==null)initializeFileBrowser();
                
                
                try{RETURN_TYPE answer = fileChooser.showOpenDialog(SuitaDetails.this);
                    if (answer == RETURN_TYPE.APPROVE){
                        FileObject aFileObject = fileChooser.getSelectedFile();
                        String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
                        safeName = safeName.substring(safeName.indexOf(Repository.host)+
                                                        Repository.host.length());
                        String [] check = safeName.split("/");
                        if(check[check.length-1].equals(check[check.length-2])){
                            StringBuffer buffer = new StringBuffer();
                            for(int i=0;i<check.length-1;i++){
                                buffer.append(check[i]+"/");}
                            safeName = buffer.toString();}
                        tprescript.setText(safeName);}}
                 catch(Exception e){
                     fileChooser=null;
                     e.printStackTrace();}
            }
        });

        browse2.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evt) {
                if(fileChooser==null)initializeFileBrowser();
                try{RETURN_TYPE answer = fileChooser.showOpenDialog(SuitaDetails.this);
                    if (answer == RETURN_TYPE.APPROVE){
                        FileObject aFileObject = fileChooser.getSelectedFile();
                        String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
                        safeName = safeName.substring(safeName.indexOf(Repository.host)+
                                                        Repository.host.length());
                        String [] check = safeName.split("/");
                        if(check[check.length-1].equals(check[check.length-2])){
                            StringBuffer buffer = new StringBuffer();
                            for(int i=0;i<check.length-1;i++){
                                buffer.append(check[i]+"/");}
                            safeName = buffer.toString();}
                        tpostscript.setText(safeName);}}
                 catch(Exception e){
                     fileChooser=null;
                     e.printStackTrace();}
            }
        });

        GroupLayout layout = new GroupLayout(global);
        global.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                        .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                            .addGap(5, 5, 5)
                            .addComponent(prescript))
                        .addComponent(stoponfail, GroupLayout.PREFERRED_SIZE, 83,
                                     GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(5, 5, 5)
                        .addComponent(postscript)))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(tprescript, GroupLayout.DEFAULT_SIZE, 216, Short.MAX_VALUE)
                    .addComponent(tpostscript))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(browse1)
                    .addComponent(browse2))
                .addGap(10, 10, 10)));
                
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(stoponfail)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(prescript)
                    .addComponent(tprescript, GroupLayout.PREFERRED_SIZE, 
                                  GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(browse1))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(tpostscript, GroupLayout.PREFERRED_SIZE, 
                                  GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(browse2)
                    .addComponent(postscript))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)));}
        
    private void initComponents(ArrayList<String []> descriptions){
        global = new JPanel();
        global.setBackground(Color.WHITE);
        initGlobal();
        
        definitions.clear();
        border = BorderFactory.createTitledBorder("Global options");
        setBorder(border);
        scroll = new JScrollPane();
        defsContainer = new JPanel();
        setLayout(new BorderLayout());
        defsContainer.setBackground(new Color(255, 255, 255));
        defsContainer.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0));
        defsContainer.setLayout(new BoxLayout(defsContainer, BoxLayout.Y_AXIS));
        //scroll.setViewportView(defsContainer);
        
        defsContainer.add(suiteoptions);
        
        scroll.setViewportView(global);
        add(scroll, BorderLayout.CENTER);
        JLabel l = new JLabel("test");            
        FontMetrics metrics = l.getFontMetrics(l.getFont());
        int width = 0;
        for(int i=0;i<descriptions.size();i++){
            if(width<metrics.stringWidth(descriptions.get(i)[Repository.LABEL])){
                width = metrics.stringWidth(descriptions.get(i)[Repository.LABEL]);}}
        for(int i=0;i<descriptions.size();i++){
            String button = descriptions.get(i)[Repository.SELECTED];
            DefPanel define = new DefPanel(descriptions.get(i)[Repository.LABEL],
                                                               button,
                                                               descriptions.get(i)[Repository.ID],
                                                               width,i,this);
            definitions.add(define);
            defsContainer.add(define);}
        //setEnabled(false);
    }
           
    public int getDefsNr(){
        return definitions.size();}
        
    public ArrayList<DefPanel> getDefs(){
        return definitions;}
           
    public void clearDefs(){
        for(int i=0;i<definitions.size();i++){
            definitions.get(i).setDescription("");}}
            
    public void setParent(Item parent){ 
        for(int i=0;i<definitions.size();i++){
            definitions.get(i).setParent(parent);}}
            
    public void setSuiteDetails(){
        scroll.setViewportView(defsContainer);
        setBorderTitle("Suite options");
    }
    
    public void setGlobalDetails(){
        scroll.setViewportView(global);
        setBorderTitle("Global options");
    }
            
    public DefPanel getDefPanel(int i){
        return definitions.get(i);}
    
    public boolean stopOnFail(){
        return stoponfail.isSelected();}
        
    public void setStopOnFail(boolean value){
        stoponfail.setSelected(value);}
        
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
    }
        
        
    public void initializeFileBrowser(){
        fileChooser = new VFSJFileChooser("sftp://"+Repository.user+":"+
                                           Repository.password+"@"+Repository.host+
                                           "/home/"+Repository.user+"/twister/config/");        
        fileChooser.setFileHidingEnabled(true);
        fileChooser.setMultiSelectionEnabled(false);
        fileChooser.setFileSelectionMode(VFSJFileChooser.SELECTION_MODE.FILES_AND_DIRECTORIES);}
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
                    VFSJFileChooser fileChooser = Repository.window.mainpanel.p4.getConfig().
                                                                                getChooser();
                    try{RETURN_TYPE answer = fileChooser.showOpenDialog(DefPanel.this);
                        if (answer == RETURN_TYPE.APPROVE){
                            FileObject aFileObject = fileChooser.getSelectedFile();
                            String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
                            safeName = safeName.substring(safeName.indexOf(Repository.host)+
                                                            Repository.host.length());
                            String [] check = safeName.split("/");
                            if(check[check.length-1].equals(check[check.length-2])){
                                StringBuffer buffer = new StringBuffer();
                                for(int i=0;i<check.length-1;i++){
                                    buffer.append(check[i]+"/");}
                                safeName = buffer.toString();}
                            userDefinition.setText(safeName);
                            if(parent!=null){
                                setParentField(userDefinition.getText(),false);}
                        }}
                    catch(Exception e){
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
//             container.setTitle("Suite "+
//                                 parent.getName());
            container.setTitle("Suite options");
            container.setEnabled(true);}
        else{
            //container.setEnabled(false);
            container.setTitle("Global options");}
        this.parent = parent;}
        
    public String getDescription(){
        return descriptions;}
    
    public void setDescription(String desc){
        userDefinition.setText(desc);}}