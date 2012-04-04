import java.util.ArrayList;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Graphics;
import javax.swing.border.BevelBorder;
import javax.swing.JLabel;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import javax.swing.JButton;
import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.OutputKeys;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Element;
import java.io.File;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import java.io.FileInputStream;
import javax.swing.JList;
import javax.swing.ListSelectionModel;
import javax.swing.DefaultListModel;
import javax.swing.event.ListSelectionListener;
import javax.swing.event.ListSelectionEvent;
import javax.swing.JOptionPane;
import java.awt.Dimension;
import java.util.Vector;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeNode;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreePath;
import java.util.List;
import java.awt.FlowLayout;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.BorderFactory;
import java.awt.Color;
import javax.swing.GroupLayout;
import javax.swing.LayoutStyle.ComponentPlacement;

public class Dut extends JPanel {

    DUTExplorer explorer;
    private JPanel HWButtonsPanel;
    JPanel SettingsPanel;
    JPanel PropertiesPanel;
    private JPanel GeneralButtonsPanel;
    private JPanel MainPanel;
    private JScrollPane jScrollPane2;
    private JScrollPane jScrollPane3;
    JScrollPane jScrollPane4;
    JButton additem;
    JButton remitem;
    int x1,y1;
    JPanel p2,propertys,propertys2,propertys3,p3,p4;;
    Device temp;
    DeviceModule temp2; 
    DevicePort temp3; 
    DefaultMutableTreeNode nodetemp1,nodetemp2,nodetemp3;
    JTextArea tdescription;
    JTextField propvalue,propvalue2,tname,tname2,tname3,tname4,propname,propvalue3,propname2,propname3,tid,tvendor,ttype,tfamily,tmodel;
    
    public Dut(){
        initComponents();
        load("hwconfig.xml");}
    
    private void initComponents() {
        explorer = new DUTExplorer();
        p4 = new JPanel();
        p4.setLayout(null);
        p4.setPreferredSize(new Dimension(400,110));
        JLabel PropName3 = new JLabel("Prop. Name");
        JLabel PropValue3 = new JLabel("Prop. Value");
        PropName3.setBounds(5,55,100,25);
        PropValue3.setBounds(160,55,100,25);
        p4.add(PropName3);
        p4.add(PropValue3);
        propname3 = new JTextField();
        propname3.setBounds(0,80,150,25);
        p4.add(propname3);
        propvalue3 = new JTextField();
        propvalue3.setBounds(155,80,160,25);
        p4.add(propvalue3);
        JButton add3 = new JButton("Add");
        add3.setBounds(330,75,58,24);
        add3.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(temp3!=null&&!propname3.getText().equals("")&&!propvalue3.getText().equals("")&&!checkForNumber(propname3.getText().charAt(0))){
                    temp3.propertys.add(new String[]{propname3.getText(),propvalue3.getText()});
                    propname3.setText("");
                    propvalue3.setText("");
                    temp3.updatePropertys();}}});
        p4.add(add3);            
        JLabel id3 = new JLabel("Port: ");
        id3.setBounds(5,5,50,20);
        tname3 = new JTextField();
        tname3.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp3!=null){
                    temp3.setPort(tname3.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp3);}}});
        tname3.setBounds(90,5,200,20);
        p4.add(id3);
        p4.add(tname3);        
        JLabel id4 = new JLabel("Port Type: ");
        id4.setBounds(5,30,70,20);
        p4.add(id4);            
        tname4 = new JTextField();
        tname4.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp3!=null){
                    temp3.setPortType(tname4.getText());
                    ((DefaultMutableTreeNode)nodetemp3.getChildAt(0)).setUserObject("Port type: "+tname4.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp3.getChildAt(0));}}});
        tname4.setBounds(90,30,200,20);
        p4.add(id4);
        p4.add(tname4); 
        JPanel fpropertys3 = new JPanel();
        fpropertys3.setLayout(null);
        fpropertys3.setBorder(BorderFactory.createTitledBorder("Properties"));
        fpropertys3.setBounds(2,105,388,530);
        propertys3 = new JPanel();
        propertys3.setLayout(null);
        JScrollPane scrollPane7 = new JScrollPane(propertys3);
        scrollPane7.setBounds(3,17,382,310);
        scrollPane7.setBorder(null);
        fpropertys3.add(scrollPane7);
        p3 = new JPanel();
        p3.setLayout(null);
        p3.setPreferredSize(new Dimension(400,110));
        JLabel PropName2 = new JLabel("Prop. Name");
        JLabel PropValue2 = new JLabel("Prop. Value");
        PropName2.setBounds(5,35,100,25);
        PropValue2.setBounds(160,35,100,25);
        p3.add(PropName2);
        p3.add(PropValue2);
        propname2 = new JTextField();
        propname2.setBounds(0,60,150,25);
        p3.add(propname2);
        propvalue2 = new JTextField();
        propvalue2.setBounds(155,60,160,25);
        p3.add(propvalue2);
        JButton add2 = new JButton("Add");
        add2.setBounds(330,65,58,24);
        add2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(temp2!=null&&!propname2.getText().equals("")&&!propvalue2.getText().equals("")&&!checkForNumber(propname2.getText().charAt(0))){
                    temp2.propertys.add(new String[]{propname2.getText(),propvalue2.getText()});
                    propname2.setText("");
                    propvalue2.setText("");
                    temp2.updatePropertys();}}});
        p3.add(add2);
        JLabel id2 = new JLabel("Module Type: ");
        id2.setBounds(5,5,80,20);
        p3.add(id2);
        tname2 = new JTextField();
        tname2.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp2!=null){
                    temp2.setName(tname2.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp2);
                    ((DefaultMutableTreeNode)nodetemp2.getChildAt(0)).setUserObject("Module Type: "+tname2.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp2.getChildAt(0));}}});
        tname2.setBounds(90,5,200,20);
        p3.add(tname2);
        JPanel fpropertys2 = new JPanel();
        fpropertys2.setLayout(null);
        fpropertys2.setBorder(BorderFactory.createTitledBorder("Properties"));
        fpropertys2.setBounds(2,95,388,540);
        propertys2 = new JPanel();
        propertys2.setLayout(null);
        JScrollPane scrollPane4 = new JScrollPane(propertys2);
        scrollPane4.setBounds(3,17,382,310);
        scrollPane4.setBorder(null);
        fpropertys2.add(scrollPane4);
        p2 = new JPanel();
        p2.setLayout(null);
        p2.setPreferredSize(new Dimension(400,270));       
        propertys = new JPanel();
        propertys.setLayout(null);
        JLabel id = new JLabel("ID: ");
        id.setBounds(5,5,50,20);
        p2.add(id);
        JLabel name = new JLabel("Name: ");
        name.setBounds(5,30,50,20);
        p2.add(name);
        JLabel vendor = new JLabel("Vendor: ");
        vendor.setBounds(5,110,50,20);
        p2.add(vendor);
        JLabel type = new JLabel("Type: ");
        type.setBounds(5,135,50,20);
        p2.add(type);
        JLabel family = new JLabel("Family: ");
        family.setBounds(5,160,50,20);
        p2.add(family);
        JLabel model = new JLabel("Model: ");
        model.setBounds(5,185,50,20);
        p2.add(model);        
        JLabel PropName = new JLabel("Prop. Name");
        JLabel PropValue = new JLabel("Prop. Value");
        PropName.setBounds(5,205,150,25);
        PropValue.setBounds(160,205,150,25);
        p2.add(PropName);
        p2.add(PropValue);
        propname = new JTextField();
        propname.setBounds(5,230,150,25);
        p2.add(propname);
        propvalue = new JTextField();
        propvalue.setBounds(160,230,160,25);
        p2.add(propvalue);
        JButton add = new JButton("Add");
        add.setBounds(330,230,58,24);
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(temp!=null&&!propname.getText().equals("")&&!propvalue.getText().equals("")&&!checkForNumber(propname.getText().charAt(0))){
                    temp.propertys.add(new String[]{propname.getText(),propvalue.getText()});
                    propname.setText("");
                    propvalue.setText("");
                    temp.updatePropertys();}}});
        p2.add(add);
        tname = new JTextField();
        tname.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp!=null){
                    temp.setName(tname.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp1);}}});
        tname.setBounds(90,30,200,20);
        p2.add(tname);
        tid = new JTextField();
        tid.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp!=null){
                    temp.setID(tid.getText());
                    ((DefaultMutableTreeNode)nodetemp1.getChildAt(0)).setUserObject("Id: "+tid.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp1.getChildAt(0));}}});
        tid.setBounds(90,5,200,20);
        p2.add(tid);
        tvendor = new JTextField();
        tvendor.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp!=null){
                    temp.setVendor(tvendor.getText());                    
                    ((DefaultMutableTreeNode)nodetemp1.getChildAt(2)).setUserObject("Vendor: "+tvendor.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp1.getChildAt(2));}}});
        tvendor.setBounds(90,110,200,20);
        p2.add(tvendor);
        ttype = new JTextField();
        ttype.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp!=null){temp.setType(ttype.getText());
                ((DefaultMutableTreeNode)nodetemp1.getChildAt(3)).setUserObject("Type: "+ttype.getText());
                ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp1.getChildAt(3));}}});
        ttype.setBounds(90,135,200,20);
        p2.add(ttype);
        tfamily = new JTextField();
        tfamily.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp!=null){
                    temp.setFamily(tfamily.getText());
                    ((DefaultMutableTreeNode)nodetemp1.getChildAt(4)).setUserObject("Family: "+tfamily.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp1.getChildAt(4));}}});
        tfamily.setBounds(90,160,200,20);
        p2.add(tfamily);
        tmodel = new JTextField();
        tmodel.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp!=null){
                    temp.setModel(tmodel.getText());
                    ((DefaultMutableTreeNode)nodetemp1.getChildAt(5)).setUserObject("Model: "+tmodel.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp1.getChildAt(5));}}});
        tmodel.setBounds(90,185,200,20);
        p2.add(tmodel);
        JLabel description = new JLabel("Description: ");
        description.setBounds(5,55,90,20);
        p2.add(description);
        tdescription = new JTextArea();
        tdescription.setLineWrap(true);
        tdescription.setWrapStyleWord(true);
        tdescription.setBounds(90,55,200,50);
        tdescription.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(temp!=null){
                    temp.setDescription(tdescription.getText());
                    ((DefaultMutableTreeNode)nodetemp1.getChildAt(1)).setUserObject("Description: "+tdescription.getText());
                    ((DefaultTreeModel)explorer.tree.getModel()).nodeChanged(nodetemp1.getChildAt(1));}}});
        p2.add(tdescription);
        try{Repository.c.cd(Repository.REMOTEHARDWARECONFIGDIRECTORY);}
        catch(Exception e){System.out.println("Could not get: "+Repository.REMOTEHARDWARECONFIGDIRECTORY+" as REMOTE HARDWARE CONFIG DIRECTORY");}
        try{System.out.println(Repository.c.pwd());}
        catch(Exception e){}   
        jScrollPane2 = new JScrollPane();
        MainPanel = new JPanel();
        jScrollPane3 = new JScrollPane();
        HWButtonsPanel = new JPanel();
        SettingsPanel = new JPanel();
        PropertiesPanel = new JPanel();
        jScrollPane4 = new JScrollPane();
        GeneralButtonsPanel = new JPanel();
        JButton save = new JButton("Save");
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                save();}});
        additem = new JButton("Add device");
        additem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addItem();}});
        remitem = new JButton("Remove Item");
        remitem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeItem();}});
        remitem.setEnabled(false);
        JButton load = new JButton("Load");
        load.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){load(null);}});
        JButton generate = new JButton("Generate");
        generate.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                generate();}});
        MainPanel.setMinimumSize(new Dimension(0, 0));
        MainPanel.setPreferredSize(new Dimension(600, 400));
        jScrollPane3.setViewportView(explorer.tree);
        PropertiesPanel.setMinimumSize(new Dimension(0, 0));
        PropertiesPanel.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Properties"));
        jScrollPane4.setBorder(null);
        GroupLayout PropertiesPanelLayout = new GroupLayout(PropertiesPanel);
        PropertiesPanel.setLayout(PropertiesPanelLayout);
        PropertiesPanelLayout.setHorizontalGroup(
            PropertiesPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGap(0, 402, Short.MAX_VALUE)
            .addGroup(PropertiesPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                .addComponent(jScrollPane4, GroupLayout.Alignment.TRAILING, GroupLayout.DEFAULT_SIZE, 251, Short.MAX_VALUE)));
        PropertiesPanelLayout.setVerticalGroup(
            PropertiesPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGap(0, 121, Short.MAX_VALUE)
            .addGroup(PropertiesPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                .addComponent(jScrollPane4, GroupLayout.DEFAULT_SIZE, 121, Short.MAX_VALUE)));
        GroupLayout MainPanelLayout = new GroupLayout(MainPanel);
        MainPanel.setLayout(MainPanelLayout);
        MainPanelLayout.setHorizontalGroup(
            MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(MainPanelLayout.createSequentialGroup()
                .addGap(10, 10, 10)
                .addGroup(MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(HWButtonsPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jScrollPane3, GroupLayout.DEFAULT_SIZE, 172, Short.MAX_VALUE))
                .addPreferredGap(ComponentPlacement.RELATED)
                .addGroup(MainPanelLayout.createParallelGroup(GroupLayout.Alignment.TRAILING, false)
                    .addComponent(PropertiesPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(SettingsPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(GeneralButtonsPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap()));
        MainPanelLayout.setVerticalGroup(
            MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GroupLayout.Alignment.TRAILING, MainPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(MainPanelLayout.createSequentialGroup()
                        .addComponent(SettingsPanel, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(ComponentPlacement.RELATED)
                        .addComponent(PropertiesPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .addComponent(jScrollPane3))
                .addPreferredGap(ComponentPlacement.RELATED)
                .addGroup(MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING, false)
                    .addComponent(GeneralButtonsPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(HWButtonsPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap()));
        jScrollPane2.setViewportView(MainPanel);
        GroupLayout layout = new GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane2));
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane2, GroupLayout.DEFAULT_SIZE, 555, Short.MAX_VALUE));
        HWButtonsPanel.add(additem);
        HWButtonsPanel.add(remitem);
        HWButtonsPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
        GeneralButtonsPanel.add(generate); 
        GeneralButtonsPanel.add(load);
        GeneralButtonsPanel.add(save);}
        
    public void save(){
        String name = JOptionPane.showInputDialog("File Name :");
        if(name!=null){
            try{DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
                DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
                Document document = documentBuilder.newDocument();
                TransformerFactory transformerFactory = TransformerFactory.newInstance();
                Transformer transformer = transformerFactory.newTransformer();
                transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
                transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
                DOMSource source = new DOMSource(document);
                Element root = document.createElement("root");
                document.appendChild(root);
                for(int i=0;i<((TreeNode)explorer.tree.getModel().getRoot()).getChildCount();i++){
                    Element em = document.createElement("device");
                    root.appendChild(em);
                    traverseTree(((TreeNode)explorer.tree.getModel().getRoot()).getChildAt(i),em,document);}
                File file = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"HardwareConfig"+Repository.getBar()+name+".xml");
                Result result = new StreamResult(file); 
                try{transformer.transform(source, result);
                    try{Repository.c.cd(Repository.REMOTEHARDWARECONFIGDIRECTORY);}
                    catch(Exception e){System.out.println("could not get "+Repository.REMOTEHARDWARECONFIGDIRECTORY);}
                    FileInputStream in = new FileInputStream(file);
                    Repository.c.put(in, file.getName());
                    in.close();}
                catch(Exception e){e.printStackTrace();
                System.out.println("Could not save in file : "+file.getCanonicalPath()+" and sen to "+Repository.REMOTEHARDWARECONFIGDIRECTORY);}} 
            catch(Exception e) {e.printStackTrace();}}}
        
    public void addItem(){
        if(additem.getText().equals("Add device")){
            explorer.addDevice();}
        else if(additem.getText().equals("Add module")){
            explorer.addModule(nodetemp1);}
        else if(additem.getText().equals("Add port")){
            explorer.addPort(nodetemp2);}}
        
    public void removeItem(){
        if(remitem.getText().equals("Remove device")){
            explorer.removeElement(nodetemp1);}
        else if(remitem.getText().equals("Remove module")){
            explorer.removeElement(nodetemp2);}
        else if(remitem.getText().equals("Remove port")){
            explorer.removeElement(nodetemp3);}
        clearSelection();}
        
    public void generate(){
        try{String status="";
            try{status = (String)Repository.frame.mainpanel.p2.client.execute("getExecStatusAll",new Object[]{});}
            catch(Exception e){System.out.println("Could not connect to server");}
            if(!status.equals("running")){
                DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
                DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
                Document document = documentBuilder.newDocument();
                TransformerFactory transformerFactory = TransformerFactory.newInstance();
                Transformer transformer = transformerFactory.newTransformer();
                transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
                transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
                DOMSource source = new DOMSource(document);
                Element root = document.createElement("Root");
                document.appendChild(root);
                for(int i=0;i<((TreeNode)explorer.tree.getModel().getRoot()).getChildCount();i++){
                    Element em = document.createElement("device");
                    root.appendChild(em);
                    traverseTree(((TreeNode)explorer.tree.getModel().getRoot()).getChildAt(i),em,document);}
                File file = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"HardwareConfig"+Repository.getBar()+"hwconfig.xml");
                Result result = new StreamResult(file); 
                try{transformer.transform(source, result);
                    try{Repository.c.cd(Repository.REMOTEHARDWARECONFIGDIRECTORY);}
                    catch(Exception e){System.out.println("could not get "+Repository.REMOTEHARDWARECONFIGDIRECTORY);}
                    FileInputStream in = new FileInputStream(file);
                    Repository.c.put(in, file.getName());
                    in.close();}
                catch(Exception e){e.printStackTrace();
                System.out.println("Could not save in file : "+file.getCanonicalPath()+" and send to "+Repository.REMOTEHARDWARECONFIGDIRECTORY);}}
            else{JOptionPane.showMessageDialog(Repository.frame, "Please close Central Engine before generating");}}
        catch(Exception e) {e.printStackTrace();}}
        
    private void load(String file){
        try{String config;
            if(file == null){
                try{Repository.c.cd(Repository.REMOTEHARDWARECONFIGDIRECTORY);}
                catch(Exception e){System.out.println("Could not get: "+Repository.REMOTEHARDWARECONFIGDIRECTORY+" as REMOTE HARDWARE CONFIG DIRECTORY");}
                Vector <LsEntry> files = Repository.c.ls(Repository.REMOTEHARDWARECONFIGDIRECTORY);
                int size = files.size();
                ArrayList<String> temp = new ArrayList<String>();
                for(int i=0;i<size;i++){
                    String name = files.get(i).getFilename();
                    if(name.split("\\.").length==0)continue; 
                    if(name.indexOf(".xml")==-1)continue;                
                    temp.add(name);}
                String configs [] = new String[temp.size()];
                temp.toArray(configs);
                config = (String)JOptionPane.showInputDialog(null, "Please select a DUT file", "Config", 1, null, configs, "Configs");}
            else config=file;
            if(config!=null){
                InputStream in=null;
                try{in = Repository.c.get(config);}
                catch(Exception e){System.out.println("Please check the hwconfig file "+config+" in "+Repository.c.pwd());}
                byte [] data = new byte[100];
                ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                int nRead;
                while ((nRead = in.read(data, 0, data.length)) != -1){buffer.write(data, 0, nRead);}
                buffer.flush();
                File theone = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"HardwareConfig"+Repository.getBar()+config);
                FileOutputStream out = new FileOutputStream(theone);
                buffer.writeTo(out);
                out.close();
                buffer.close();
                in.close();
                DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
                DocumentBuilder db = dbf.newDocumentBuilder();
                Document doc = null;
                try{doc = db.parse(theone);}
                catch(Exception e){System.out.println(theone.getCanonicalPath()+" is corrupted or incomplete");}
                if(doc!=null){
                    doc.getDocumentElement().normalize();                
                    NodeList nodeLst = doc.getElementsByTagName("device");
                    int childsnr = nodeLst.getLength();
                    if(childsnr>0){
                        while(((DefaultMutableTreeNode)explorer.tree.getModel().getRoot()).getChildCount()>0){
                            ((DefaultTreeModel)explorer.tree.getModel()).removeNodeFromParent((DefaultMutableTreeNode)(((DefaultMutableTreeNode)explorer.tree.getModel().getRoot()).getChildAt(0)));}
                        for(int i = 0;i<childsnr;i++){
                            Node node = nodeLst.item(i);
                            Device d = new Device();
                            try{d.setName(((Element)node).getElementsByTagName("devicename").item(0).getChildNodes().item(0).getNodeValue());}
                            catch(Exception e){d.setName("");}
                            DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
                            ((DefaultMutableTreeNode)(explorer.tree.getModel().getRoot())).add(child);                                    
                            try{d.setID(((Element)node).getElementsByTagName("deviceid").item(0).getChildNodes().item(0).getNodeValue());}
                            catch(Exception e){d.setID("");}
                            DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Id: "+d.id,false);
                            child.add(child3);                                    
                            try{d.setDescription(((Element)node).getElementsByTagName("devicedesc").item(0).getChildNodes().item(0).getNodeValue());}
                            catch(Exception e){d.setDescription("");}
                            DefaultMutableTreeNode child2 = new DefaultMutableTreeNode("Description: "+d.description,false);
                            child.add(child2);
                            try{d.setVendor(((Element)node).getElementsByTagName("devicevendor").item(0).getChildNodes().item(0).getNodeValue());}
                            catch(Exception e){d.setVendor("");}
                            DefaultMutableTreeNode child4 = new DefaultMutableTreeNode("Vendor: "+d.vendor,false);
                            child.add(child4);
                            try{d.setType(((Element)node).getElementsByTagName("devicetype").item(0).getChildNodes().item(0).getNodeValue());}
                            catch(Exception e){d.setType("");}
                            DefaultMutableTreeNode child5 = new DefaultMutableTreeNode("Type: "+d.type,false);
                            child.add(child5);
                            try{d.setFamily(((Element)node).getElementsByTagName("devicefamily").item(0).getChildNodes().item(0).getNodeValue());}
                            catch(Exception e){d.setFamily("");}
                            DefaultMutableTreeNode child6 = new DefaultMutableTreeNode("Family: "+d.family,false);
                            child.add(child6);
                            try{d.setModel(((Element)node).getElementsByTagName("devicemodel").item(0).getChildNodes().item(0).getNodeValue());}
                            catch(Exception e){d.setModel("");}
                            DefaultMutableTreeNode child7 = new DefaultMutableTreeNode("Model: "+d.model,false);
                            child.add(child7);
                            if(((Element)node).getChildNodes().getLength()>15){
                                for(int j=15;j<((Element)node).getChildNodes().getLength();j++){
                                    if(((Element)node).getChildNodes().item(j).getNodeName().equals("devicemodule"))break;
                                    d.propertys.add(new String[]{((Element)node).getChildNodes().item(j).getNodeName(),((Element)node).getChildNodes().item(j).getChildNodes().item(0).getNodeValue()});
                                    DefaultMutableTreeNode child8 = new DefaultMutableTreeNode(((Element)node).getChildNodes().item(j).getNodeName()+" - "+((Element)node).getChildNodes().item(j).getChildNodes().item(0).getNodeValue(),false);
                                    child.add(child8);
                                    j++;}}
                            if(((Element)node).getElementsByTagName("devicemodule").getLength()>0){
                                NodeList listamodule = ((Element)node).getElementsByTagName("devicemodule");
                                for(int k=0;k<listamodule.getLength();k++){
                                    DeviceModule dmodul = new DeviceModule("");
                                    d.addModule(dmodul);
                                    DefaultMutableTreeNode child8 = new DefaultMutableTreeNode(dmodul);
                                    child.add(child8);
                                    Node modul = listamodule.item(k);
                                    if(((Element)modul).getElementsByTagName("moduletype").getLength()>0){
                                            try{dmodul.setName(((Element)node).getElementsByTagName("moduletype").item(0).getChildNodes().item(0).getNodeValue());}
                                            catch(Exception e){dmodul.setName("");}
                                            DefaultMutableTreeNode child9 = new DefaultMutableTreeNode("Module Type: "+dmodul.name,false);
                                            child8.add(child9);}
                                    else{DefaultMutableTreeNode child9 = new DefaultMutableTreeNode("Module Type: ",false);// in cazul in care nu are tag modultype
                                        child8.add(child9);}
                                    for(int l=3;l<((Element)modul).getChildNodes().getLength();l++){
                                        if(((Element)modul).getChildNodes().item(l).getNodeName().equals("deviceport"))break;
                                        else{dmodul.propertys.add(new String[]{((Element)modul).getChildNodes().item(l).getNodeName(),((Element)modul).getChildNodes().item(l).getChildNodes().item(0).getNodeValue()});
                                            DefaultMutableTreeNode child10 = new DefaultMutableTreeNode(((Element)modul).getChildNodes().item(l).getNodeName()+" - "+((Element)modul).getChildNodes().item(l).getChildNodes().item(0).getNodeValue(),false);
                                            child8.add(child10);}
                                        l++;}
                                    if(((Element)modul).getElementsByTagName("deviceport").getLength()>0){
                                        NodeList listaporturi = ((Element)modul).getElementsByTagName("deviceport");
                                        for(int l=0;l<listaporturi.getLength();l++){
                                            Node port = listaporturi.item(l);
                                            DevicePort dport = null;
                                            try{dport = new DevicePort(((Element)port).getElementsByTagName("port").item(0).getChildNodes().item(0).getNodeValue(),((Element)port).getElementsByTagName("portType").item(0).getChildNodes().item(0).getNodeValue());}
                                            catch(Exception e){dport = new DevicePort("","");}
                                            dmodul.addPort(dport);
                                            DefaultMutableTreeNode child11 = new DefaultMutableTreeNode(dport,true);
                                            child8.add(child11);                                                    
                                            DefaultMutableTreeNode child13 = new DefaultMutableTreeNode("Port type: "+dport.portType,false);
                                            child11.add(child13);
                                            for(int m=5;m<((Element)port).getChildNodes().getLength();m++){
                                                Node prop = ((Element)port).getChildNodes().item(m);
                                                dport.propertys.add(new String[]{((Element)prop).getNodeName(),((Element)prop).getChildNodes().item(0).getNodeValue()});
                                                DefaultMutableTreeNode child14 = new DefaultMutableTreeNode(((Element)prop).getNodeName()+" - "+((Element)prop).getChildNodes().item(0).getNodeValue(),false);
                                                child11.add(child14);
                                                m++;}}}}}
                            ((DefaultTreeModel)explorer.tree.getModel()).reload();}
                        clearSelection();}
                else System.out.println(theone.getCanonicalPath()+" has no devices");}}}
        catch(Exception e){e.printStackTrace();}}
        
    public void clearSelection(){
        nodetemp3 = null; 
        nodetemp2 = null; 
        nodetemp1 = null; 
        remitem.setEnabled(false);
        additem.setEnabled(true);
        additem.setText("Add device");
        remitem.setText("Remove item");
        SettingsPanel.remove(p2);
        SettingsPanel.remove(p3);
        SettingsPanel.remove(p4);
        jScrollPane4.setViewportView(null);}        
        
    public void traverseTree(TreeNode t,Element root,Document document){
        System.out.println(t.toString());
        Element theone = root;
        if(((DefaultMutableTreeNode)t).getUserObject() instanceof DeviceModule){
            theone = document.createElement("devicemodule");
            System.out.println("devicemodule");
            root.appendChild(theone);}
        else if(((DefaultMutableTreeNode)t).getUserObject() instanceof DevicePort){
            theone = document.createElement("deviceport");
            System.out.println("deviceport");
            root.appendChild(theone);}
        else if(((DefaultMutableTreeNode)t).getUserObject() instanceof Device){
            System.out.println("device");}
        else{
            if(root.getNodeName().equals("device")){
                if(((String)((DefaultMutableTreeNode)t).getUserObject()).indexOf("Id: ")!=-1){
                    Element em = addElement(document, t, root,"deviceid","Id: ", 1);
                    Element em2 = document.createElement("devicename");                    
                    try{em2.appendChild(document.createTextNode(((DefaultMutableTreeNode)((DefaultMutableTreeNode)t).getParent()).getUserObject().toString().split("Device: ")[1]));}
                    catch(Exception e){em.appendChild(document.createTextNode(""));}
                    root.appendChild(em2);}
                else if(((String)((DefaultMutableTreeNode)t).getUserObject()).indexOf("Description: ")!=-1){
                    addElement(document, t, root,"devicedesc","Description: ", 1);}
                else if(((String)((DefaultMutableTreeNode)t).getUserObject()).indexOf("Vendor: ")!=-1){
                    addElement(document, t, root,"devicevendor","Vendor: ", 1);}
                else if(((String)((DefaultMutableTreeNode)t).getUserObject()).indexOf("Type: ")!=-1){
                    addElement(document, t, root,"devicetype","Type: ", 1);}
                else if(((String)((DefaultMutableTreeNode)t).getUserObject()).indexOf("Family: ")!=-1){
                    addElement(document, t, root,"devicefamily","Family: ", 1);}
                else if(((String)((DefaultMutableTreeNode)t).getUserObject()).indexOf("Model: ")!=-1){
                    addElement(document, t, root,"devicemodel","Model: ", 1);}
                else{getProp(t,document,root);}}
            if(root.getNodeName().equals("devicemodule")){
                if(((String)((DefaultMutableTreeNode)t).getUserObject()).indexOf("Module Type: ")!=-1){
                    Element em2 = document.createElement("moduletype");                    
                    try{em2.appendChild(document.createTextNode(((DefaultMutableTreeNode)((DefaultMutableTreeNode)t).getParent()).getUserObject().toString().split("Module: ")[1]));}
                    catch(Exception e){em2.appendChild(document.createTextNode(""));}
                    root.appendChild(em2);}
                else{getProp(t,document,root);}}
            if(root.getNodeName().equals("deviceport")){                
                if(((String)((DefaultMutableTreeNode)t).getUserObject()).indexOf("Port type: ")!=-1){
                    Element em2 = document.createElement("port");                    
                    try{em2.appendChild(document.createTextNode(((DefaultMutableTreeNode)((DefaultMutableTreeNode)t).getParent()).getUserObject().toString().split("Port: ")[1]));}
                    catch(Exception e){em2.appendChild(document.createTextNode(""));}
                    root.appendChild(em2);
                    Element em = document.createElement("portType");
                    try{em.appendChild(document.createTextNode(((String)((DefaultMutableTreeNode)t).getUserObject()).split("Port type: ")[1]));}
                    catch(Exception e){em.appendChild(document.createTextNode(""));}
                    root.appendChild(em);}
                else{getProp(t,document,root);}}}
        for(int i=0;i<t.getChildCount();i++){
            traverseTree(t.getChildAt(i),theone,document);}}
            
    public Element addElement(Document document,TreeNode t,Element root,String tag,String split, int index){
        Element em = document.createElement(tag);
        try{em.appendChild(document.createTextNode(((String)((DefaultMutableTreeNode)t).getUserObject()).split(split)[index]));}
        catch(Exception e){em.appendChild(document.createTextNode(""));}
        root.appendChild(em);
        return em;}
        
    public boolean checkForNumber(char a){
        try{Integer.parseInt(a+"");
            return true;}
        catch(Exception e){return false;}}
        
    public void getProp(TreeNode t,Document document,Element root){
        String name=""; 
        try{name=((String)((DefaultMutableTreeNode)t).getUserObject()).split(" - ")[0];}
        catch(Exception e){name="null";}
        String value = "";
        try{value= ((String)((DefaultMutableTreeNode)t).getUserObject()).split(" - ")[1];}
        catch(Exception e){value="null";}
        if(name.equals(""))name="null";
        if(value.equals(""))value="null";    
        System.out.println("NAME: "+name);
        Element em = document.createElement(""+name);
        em.appendChild(document.createTextNode(value));
        root.appendChild(em);}}