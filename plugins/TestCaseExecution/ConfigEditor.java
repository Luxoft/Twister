/*
File: ConfigEditor.java ; This file is part of Twister.
Version: 2.007

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
import javax.swing.DropMode;
import javax.swing.TransferHandler;
import javax.swing.JComponent;
import java.awt.datatransfer.Transferable;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.UnsupportedFlavorException;
import java.util.HashMap;
import java.awt.datatransfer.DataFlavor;
import javax.swing.JTree;
import javax.swing.JScrollPane;
import javax.swing.tree.DefaultMutableTreeNode;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathFactory;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathConstants;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import javax.swing.tree.DefaultTreeModel;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.tree.TreePath;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import com.twister.CustomDialog;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import javax.swing.JTextField;
import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.BoxLayout;
import java.awt.BorderLayout;
import java.io.FileInputStream;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.Channel;
import java.util.Properties;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import javax.swing.JButton;
import javax.swing.event.AncestorEvent;
import javax.swing.event.AncestorListener;
import java.io.BufferedWriter;
import java.io.FileWriter;
import javax.swing.GroupLayout;
import javax.swing.LayoutStyle;
import javax.swing.JTextArea;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import java.awt.event.KeyListener;
import javax.swing.JComboBox;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import javax.swing.JFormattedTextField;
import javax.swing.text.MaskFormatter;
import javax.swing.text.DefaultFormatterFactory;
import javax.swing.text.PlainDocument;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.PlainDocument;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import javax.swing.DefaultComboBoxModel;
import javax.swing.border.BevelBorder;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.Color;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import com.twister.MySftpBrowser;
import javax.swing.AbstractAction;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import javax.swing.JSplitPane;
import javax.swing.SwingUtilities;
import java.io.Writer;
import java.io.StringWriter;
import javax.xml.bind.DatatypeConverter;
import org.xml.sax.InputSource;
import java.io.StringReader;
import java.util.Enumeration;

public class ConfigEditor extends JPanel{
    public ChannelSftp ch ;
    public Session session;    
    public JScrollPane panel;
    public JPanel pdesc;
    private JTree tree;
    private XPath xpath;
    private Document doc;
    private DefaultMutableTreeNode root;
    private boolean finished = true;
    private JButton addconf,addparam,remove,unbind,save, saveas;
    public JButton close;
    private JLabel cname;
    private JTextArea tdescription;
    private JTextField tvalue, tname;
    private JComboBox ttype;
    private IntegerRangeDocument docum;
    private MyFocusAdapter focusadapter;
    private File currentfile;
    private String remotelocation;
    public ConfigTree cfgtree;
    private JLabel displayname;
    private JScrollPane jScrollPane1;
    public JPanel sutpanel;
    private Document bindingdoc;
    private boolean editable;
    private boolean lastsave = true;
    public SutConfig sutconfig;
    
    public ConfigEditor(){
        initSftp();
        init();
    }
    
    public void parseDocument(File file){
        try{this.currentfile = file;
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            if(file!=null){
                displayname.setText("Configuration file: "+file.getName());                
                try{doc = db.parse(file); 
                } catch (Exception e){
                    doc = db.newDocument();
                    doc.appendChild(doc.createElement("root"));
                }
                doc.getDocumentElement().normalize();  
            } else {
                doc = db.newDocument();
                doc.appendChild(doc.createElement("root"));
                doc.getDocumentElement().normalize();  
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    private void initParamDesc(){
        pdesc = new JPanel();
        JLabel name = new JLabel("Name:");
        JLabel description = new JLabel("Description:");
        tname = new JTextField();
        focusadapter = new MyFocusAdapter();
        tname.addFocusListener(focusadapter);
        tdescription = new JTextArea();
        JLabel value = new JLabel("Value:");
        tvalue = new JTextField();
        JLabel type = new JLabel("Type:");
        ttype = new JComboBox();
        docum = new IntegerRangeDocument(0,255,'d');
        tvalue.setDocument(docum);

        tdescription.setColumns(20);
        tdescription.setRows(5);
        tdescription.setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
        tdescription.setMinimumSize(new Dimension(6, 16));
        tdescription.setWrapStyleWord(true);
        tdescription.setLineWrap(true);

        ttype.setModel(new DefaultComboBoxModel(new String[] { "decimal", "hex", "octet", "string" }));
        ttype.setMinimumSize(new Dimension(6, 20));

        GroupLayout layout = new GroupLayout(pdesc);
        pdesc.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(10, 10, 10)
                .addComponent(description)
                .addContainerGap())
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(name)
                            .addComponent(value)
                            .addComponent(type))
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(tname, GroupLayout.Alignment.TRAILING)
                            .addComponent(tvalue, GroupLayout.Alignment.TRAILING)
                            .addComponent(ttype, GroupLayout.Alignment.TRAILING, 0, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                    .addComponent(tdescription, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap()
                )
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(name)
                    .addComponent(tname, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(value)
                    .addComponent(tvalue, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(type)
                    .addComponent(ttype, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addComponent(description)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(tdescription, GroupLayout.DEFAULT_SIZE, 104, Short.MAX_VALUE)
                .addGap(2, 2, 2)
                //.addContainerGap()
                )
        );
    }

    public void init(){
        displayname = new JLabel("Configuration file:");
        JMenuBar menubar = new JMenuBar();
        menubar.setLayout(new BorderLayout());
        menubar.setPreferredSize(new Dimension(500,18));
//         JMenu menu = new JMenu("File");
//         menu.setBounds(0,0,70,25);
//         menubar.add(menu,BorderLayout.WEST);
        JPanel temp = new JPanel();
        temp.setLayout(new BorderLayout());
        temp.add(displayname,BorderLayout.NORTH);
        
        menubar.add(temp,BorderLayout.WEST);
//         save = new JMenuItem("Save");
//         save.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 save();
//             }});
//         menu.add(save);
//         saveas = new JMenuItem("Save As");
//         saveas.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 saveAs();
//             }});
//         saveas.setEnabled(false);
//         menu.add(saveas);
        root = new DefaultMutableTreeNode("root", true);
        tree = new JTree(root);
        tree.setRootVisible(false);
        tree.setCellRenderer(new CustomIconRenderer());
        tree.setDropMode(DropMode.ON_OR_INSERT);
        tree.setDragEnabled(true);
        tree.setTransferHandler(new ImportTreeTransferHandler());
        
        JPanel cfgpanel = new JPanel();
        panel = new JScrollPane(tree);  
        cfgpanel.setLayout(new BorderLayout());
        cfgpanel.add(panel,BorderLayout.CENTER);
        
        
//         JPanel buttonLayout = new JPanel();
//         buttonLayout.setLayout(new GridBagLayout());
//         cfgpanel.add(buttonLayout,BorderLayout.SOUTH);
        
        JPanel buttonPanel = new JPanel();  
//         buttonPanel.setSize(500,35);
//         buttonPanel.setPreferredSize(new Dimension(500,35));
//         buttonPanel.setMaximumSize(new Dimension(500,35));
//         buttonPanel.setMinimumSize(new Dimension(500,35));
        addconf = new JButton("Add component");
        addconf.setEnabled(false);
        addparam = new JButton("Add property");
        remove = new JButton("Delete");
        unbind = new JButton("UnBind");
        
//         addconf.setBounds(0,5,130,25);
        buttonPanel.add(addconf);
        addconf.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addConf();
            }
        });
        
//         addparam.setBounds(140,5,140,25);
        buttonPanel.add(addparam);
        addparam.setEnabled(false);
        addparam.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addParam();
            }
        });
        
//         unbind.setBounds(395,5,100,25);
        buttonPanel.add(unbind);
        unbind.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                ((MyFolder)((DefaultMutableTreeNode)tree.getSelectionPath().getLastPathComponent()).getUserObject()).setSut(null);
                ((MyFolder)((DefaultMutableTreeNode)tree.getSelectionPath().getLastPathComponent()).getUserObject()).setSutPath (null);
                ((DefaultTreeModel)tree.getModel()).nodeChanged(((DefaultMutableTreeNode)tree.getSelectionPath().getLastPathComponent()));
            }
        });
        unbind.setEnabled(false);

//         remove.setBounds(290,5,100,25);
        remove.setEnabled(false);
        buttonPanel.add(remove);
        remove.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(acceptRemove())deleteMultiple();
            }
        });
//         buttonLayout.add(buttonPanel,new GridBagConstraints());


        save = new JButton("Save");
        saveas = new JButton("Save As");
        close = new JButton("Close");
//         save.setEnabled(false);
        saveas.setEnabled(false);
        close.setEnabled(false);
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                save();
            }
        });
        
        saveas.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                saveAs();
            }
        });
        
        close.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(editable){
                    if(!lastsave){
                        int r = (Integer)CustomDialog.showDialog(
                                    new JLabel("Save config before closing ?"),
                                    JOptionPane.QUESTION_MESSAGE, 
                                    JOptionPane.OK_CANCEL_OPTION, ConfigEditor.this, "Save", null);
                        if(r == JOptionPane.OK_OPTION){
                            save.doClick();
                        }
                    }
                    try{String resp = RunnerRepository.getRPCClient().execute("unlockConfig", new Object[]{remotelocation}).toString();
                        if(resp.indexOf("*ERROR*")!=-1){
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigEditor.this,"ERROR", resp);
                        } else {
                             cfgtree.releaseConfig(remotelocation);
                        }
                    } catch(Exception e){e.printStackTrace();}
                    //cfgtree.refreshStructure();
                }
                reinitialize();
                saveas.setEnabled(false);
                close.setEnabled(false);
                getBinding("default");
                interpretBinding();
                lastsave = true;
            }
        });
        
        buttonPanel.add(save);
        buttonPanel.add(saveas);
        buttonPanel.add(close);
        



//         JPanel temp2 = new JPanel();
//         temp2.setLayout(new BorderLayout());
        //temp2.add(buttonPanel,BorderLayout.WEST);
//         cfgpanel.add(temp2,BorderLayout.SOUTH);
        initParamDesc();
        this.setLayout(new BorderLayout());
//         this.add(temp,BorderLayout.NORTH);
        this.add(menubar,BorderLayout.NORTH);
        //this.add(panel,BorderLayout.CENTER);
        
//         jScrollPane1 = new JScrollPane();
        
        sutpanel = new JPanel();
        sutpanel.setLayout(new BorderLayout());
//         sutpanel.add(jScrollPane1, BorderLayout.CENTER);
        sutconfig = new SutConfig();
        sutpanel.add(sutconfig, BorderLayout.CENTER);
        JButton refreshsut = new JButton("Refresh");
        refreshsut.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sutconfig.getFirstLevel();
            }
        });
        JPanel refreshpanel = new JPanel();
        refreshpanel.add(refreshsut);
        sutpanel.add(refreshpanel, BorderLayout.SOUTH);
        
//         final JSplitPane sp = new JSplitPane();
//         sp.setLeftComponent(panel);
//         sp.setRightComponent(sutpanel);
//         sp.setOrientation(JSplitPane.HORIZONTAL_SPLIT);
//         sp.setResizeWeight(0.5);
//         SwingUtilities.invokeLater(new Runnable() {
//             public void run() {
//                 sp.setDividerLocation(0.5);
//             }
//         });
        
        this.add(cfgpanel,BorderLayout.CENTER);
        this.add(buttonPanel,BorderLayout.SOUTH);
            
        JPanel bottompanel = new JPanel();
        bottompanel.setLayout(new BorderLayout());
       
        bottompanel.add(pdesc,BorderLayout.CENTER);
        this.add(bottompanel,BorderLayout.EAST);
//         GroupLayout buttonPanelLayout = new GroupLayout(buttonPanel);
//         buttonPanel.setLayout(buttonPanelLayout);
//         buttonPanelLayout.setHorizontalGroup(
//             buttonPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGap(0, 0, Short.MAX_VALUE)
//         );
//         buttonPanelLayout.setVerticalGroup(
//             buttonPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGap(0, 35, Short.MAX_VALUE)
//         );
        tree.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                TreePath tp = tree.getSelectionPath();
                if(ev.getKeyCode()==KeyEvent.VK_DELETE && (currentfile!=null || (currentfile==null && (tp.getPathCount()>2 && ((DefaultMutableTreeNode)tp.getPathComponent(1)).toString().equals("default_binding"))))){
                    if(acceptRemove())deleteMultiple();
                }
            }
        });

        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                if(!editable&&currentfile!=null)return;
                TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                if (tp != null){
                    boolean editable = true;
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        tree.setSelectionPath(tp);
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyFolder){
                            remove.setEnabled(true);
                            addconf.setEnabled(true);
                            addparam.setEnabled(true);
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            MyFolder folder = (MyFolder)treenode.getUserObject();
                            if(folder.getSut().equals("")){
                                unbind.setEnabled(false);
                            } else {
                                unbind.setEnabled(true);
                            }
                            if(currentfile==null){
                                if(!((DefaultMutableTreeNode)tp.getPathComponent(1)).toString().equals("default_binding")){
                                    remove.setEnabled(false);
                                    addconf.setEnabled(false);
                                    unbind.setEnabled(false);    
                                    editable = false;
                                }else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getLevel()==1){
                                    editable = false;
                                    remove.setEnabled(false);
                                }
                                addparam.setEnabled(false);
                            } else {
                                showFolderPopUp(treenode,ev,folder);
                            }
                            setDescription(folder.getNode(), folder.getDesc(),null,null,(DefaultMutableTreeNode)tp.getLastPathComponent(),editable);
                        }else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyParam){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            MyParam param = (MyParam)treenode.getUserObject();
                            setDescription(param.getName(),param.getDesc(),param.getType(),param.getValue(),(DefaultMutableTreeNode)tp.getLastPathComponent(),true);
                            showParamPopUp(treenode,ev,param);
                            remove.setEnabled(true);
                            addconf.setEnabled(false);
                            addparam.setEnabled(false);
                        }
                    } else if(ev.getButton() == MouseEvent.BUTTON1){
                        if(tree.getSelectionPaths().length==1){
                            tp = tree.getSelectionPath();
                            if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyFolder){
                                remove.setEnabled(true);
                                addconf.setEnabled(true);
                                addparam.setEnabled(true);
                                MyFolder folder = (MyFolder)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject();
                                if(folder.getSut().equals("")){
                                    unbind.setEnabled(false);
                                } else {
                                    unbind.setEnabled(true);
                                }
                                if(currentfile==null){
                                    if(!((DefaultMutableTreeNode)tp.getPathComponent(1)).toString().equals("default_binding")){
                                        remove.setEnabled(false);
                                        addconf.setEnabled(false);
                                        unbind.setEnabled(false);
                                        editable = false;
                                    }else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getLevel()==1){
                                        editable = false;
                                        remove.setEnabled(false);
                                    }
                                    addparam.setEnabled(false);
                                }
                                setDescription(folder.getNode(), folder.getDesc(),null,null,(DefaultMutableTreeNode)tp.getLastPathComponent(),editable);
                            }else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyParam){
                                MyParam param = (MyParam)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject();
                                setDescription(param.getName(),param.getDesc(),param.getType(),param.getValue(),(DefaultMutableTreeNode)tp.getLastPathComponent(),true);
                                remove.setEnabled(true);
                                addconf.setEnabled(false);
                                addparam.setEnabled(false);
                            }
                        } else {
                            setDescription(null,null,null,null,null,false);
                            remove.setEnabled(false);
                            addconf.setEnabled(false);
                            addparam.setEnabled(false);
                            unbind.setEnabled(false); 
                        }
                    }
                } else {
                    setDescription(null,null,null,null,null,false);
                    tree.setSelectionPath(null);
                    remove.setEnabled(false);
                    addconf.setEnabled(false);
                    if(editable&&currentfile!=null)addconf.setEnabled(true);
                    addparam.setEnabled(false);
                    unbind.setEnabled(false);
                    if(currentfile!=null){
                        if(ev.getButton() == MouseEvent.BUTTON3){
                            showNewFolderPopUp(ev);
                        }
                    }
                }
            }
        });
        parseDocument(null);
        getBinding("default");
        interpretBinding();
    }
    
    public void openedConfig(boolean editable){
        lastsave = true;
        this.editable = editable;
        if(editable){
            save.setEnabled(true);
            saveas.setEnabled(true);
        }else {
            save.setEnabled(false);
            saveas.setEnabled(false);
            addconf.setEnabled(false);
        }
        
        close.setEnabled(true);
    }
    
    public void getBinding(String filepath){
        String response = "";
        if(filepath.equals("default")){
            try{
//                 response = RunnerRepository.getRPCClient().execute("getBinding", new Object[]{RunnerRepository.user,"default_binding"}).toString();
                response = RunnerRepository.getRPCClient().execute("readFile", new Object[]{"~/twister/config/bindings.xml"}).toString();
                response = new String(DatatypeConverter.parseBase64Binary(response));
                save.setEnabled(true);
//                 content = new String(DatatypeConverter.parseBase64Binary(content));
//                 response = test.defaultbinding;
            } catch(Exception e){
                System.out.println("Could not get bindingfile from CE!");
                e.printStackTrace();
            }
        } else {
//             response = test.binding;
//         }
            try{
                filepath = filepath.replace(RunnerRepository.TESTCONFIGPATH, "");
                if(filepath.charAt(0) == '/')filepath = filepath.substring(1);
                response = RunnerRepository.getRPCClient().execute("getBinding", new Object[]{RunnerRepository.user,filepath}).toString();
                System.out.println(filepath+" -- "+response);
                
            }
                catch(Exception e){
                    System.out.println("Could not get binding for:"+filepath+" from CE");
                    e.printStackTrace();
                    return;
                }
            }
        try{
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            if(response!=null&&!response.equals("")&&!response.equalsIgnoreCase("false")&&response.indexOf("*ERROR*")==-1){
                bindingdoc = db.parse(new InputSource(new StringReader(response)));
                bindingdoc.getDocumentElement().normalize();
            } else {                
                if(response.indexOf("*ERROR*")!=-1){
                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigEditor.this,"ERROR", response);
                }
                bindingdoc = db.newDocument();
                bindingdoc.appendChild(bindingdoc.createElement("root"));
            }
        } catch(Exception e){
            System.out.println("Could not parse binding: "+response);
            e.printStackTrace();
            return;
        }
    }
    
    public void interpretBinding(){
        try{
            if(currentfile==null){//this is default binding
                displayname.setText("Configuration file: DEFAULT");
                NodeList bindings = bindingdoc.getElementsByTagName("binding");
                for(int i=0;i<bindings.getLength();i++){
                    Element binding = (Element)bindings.item(i);
                    if(binding.getElementsByTagName("name").getLength()==0)continue;
                    String filename = binding.getElementsByTagName("name").item(0).getFirstChild().getNodeValue();
                    Element rootElement = doc.createElement("folder");
                    doc.getFirstChild().appendChild(rootElement);
                    Element fname = doc.createElement("fname");
                    rootElement.appendChild(fname);  
                    Node node = doc.createTextNode(filename);
                    fname.appendChild(node);
                    MyFolder parent = new MyFolder(node);
                    DefaultMutableTreeNode treenode = new DefaultMutableTreeNode(parent,true);
                    DefaultMutableTreeNode searchin =  treenode;
                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(treenode, root,root.getChildCount());
                    NodeList binds = binding.getElementsByTagName("bind");
                    int size = binds.getLength();
                    DefaultMutableTreeNode backup = treenode;
                    for(int k=0;k<size;k++){
                        Node bind = binds.item(k);
                        String sutid = bind.getAttributes().getNamedItem("sut").getNodeValue();
                        String [] path = bind.getAttributes().getNamedItem("config").getNodeValue().split("/");
                        DefaultMutableTreeNode found = searchin;
                        for(int j=0;j<path.length;j++){
                            found = findInNode(found, path[j]);
                            if(found!=null){
                                treenode = found;
                                continue;
                            }
                            rootElement = doc.createElement("folder");
                            parent.getNode().getParentNode().getParentNode().appendChild(rootElement);
                            fname = doc.createElement("fname");
                            rootElement.appendChild(fname);  
                            node = doc.createTextNode(path[j]);
                            fname.appendChild(node);
                            parent = new MyFolder(node);
                            Element fdesc = doc.createElement("fdesc");
                            rootElement.appendChild(fdesc);
                            node = doc.createTextNode("");
                            fdesc.appendChild(node);
                            parent.setDesc(node);
                            DefaultMutableTreeNode temp = new DefaultMutableTreeNode(parent,true);
                            ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treenode,treenode.getChildCount());
                            treenode = temp;
                        }
                        parent.setSut(sutid);
                        parent.setSutPath(getPathForSut(sutid));
                        treenode = backup;
                    }
                }
            } else {
                NodeList binds = bindingdoc.getElementsByTagName("bind");
                for(int i=0;i<binds.getLength();i++){
                    Node bind = binds.item(i);
                    String sutid = bind.getAttributes().getNamedItem("sut").getNodeValue();
                    String [] path = bind.getAttributes().getNamedItem("config").getNodeValue().split("/");
                    DefaultMutableTreeNode node = (DefaultMutableTreeNode)tree.getModel().getRoot();
                    for(String el:path){
                        if(node==null)break;
                        node = findInNode(node,el);
                    }
                    if(node!=null){
                        ((MyFolder)node.getUserObject()).setSut(sutid);
                        ((MyFolder)node.getUserObject()).setSutPath(getPathForSut(sutid));
                    }
                }
            }
            ((DefaultTreeModel)tree.getModel()).reload();
        }catch(Exception e){
            System.out.println("There is an error in reading bindings: "+bindingdoc.toString());
            e.printStackTrace();
        }
    }
    
    private String getPathForSut(String sutid){
        String sutpath = "";
        Object ob = null;
        try{ob = sutconfig.client.execute("getSut", new Object[]{sutid,RunnerRepository.user,RunnerRepository.user});
            HashMap subhash= (HashMap)ob;
            sutpath = subhash.get("path").toString();
            sutpath = sutpath.replace(".system", "(system)");
            sutpath = sutpath.replace(".user", "(user)");                        
        }catch(Exception e){
            sutpath = "Sut not available!";
            System.out.println("Server response: "+ob.toString());
            e.printStackTrace();
        }
        return sutpath;
    }
    
    public void saveBinding(){
        try{
            Node first;
            if(bindingdoc!=null){
                first = bindingdoc.getFirstChild();
                NodeList list = first.getChildNodes();
                int size = list.getLength();
                if(first!=null){
                    for(int i=size-1;i>=0;i--){
                        first.removeChild(list.item(i));
                       
                }
            } else {
                DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
                DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
                bindingdoc = documentBuilder.newDocument();
                first = bindingdoc.createElement("root");
                bindingdoc.appendChild(first);
            }
            if(currentfile!=null){
                Enumeration e = root.preorderEnumeration();
                while(e.hasMoreElements()){
                    DefaultMutableTreeNode node = (DefaultMutableTreeNode)e.nextElement();
                    if(node.getUserObject() instanceof MyFolder){
                        MyFolder folder = (MyFolder)node.getUserObject();
                        if(folder.getSut()!=null && !folder.getSut().equals("")){
                            TreePath tp =  new TreePath(node.getPath());
                            size = tp.getPathCount();
                            StringBuilder sb = new StringBuilder();
                            DefaultMutableTreeNode temp;
                            for(int i=1;i<size-1;i++){
                                sb.append(((MyFolder)((DefaultMutableTreeNode)tp.getPathComponent(i)).getUserObject()).getNode().getNodeValue());
                                sb.append("/");                            
                            }
                            sb.append(folder.getNode().getNodeValue());
                            String path = sb.toString();
                            String sut = folder.getSut();
                            Element bind = bindingdoc.createElement("bind");
                            bind.setAttribute("config", path);
                            bind.setAttribute("sut", sut);
                            first.appendChild(bind);
                        }
                    }
                }
                
                TransformerFactory transformerFactory = TransformerFactory.newInstance();
                Transformer transformer = transformerFactory.newTransformer();
                transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
                transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
                DOMSource source = new DOMSource(bindingdoc);
                StringWriter writer = new StringWriter();
                StreamResult result = new StreamResult(writer);
                transformer.transform(source, result);
                String binding = writer.toString();
                String resp = RunnerRepository.getRPCClient().execute("setBinding", new Object[]{RunnerRepository.user,remotelocation,binding}).toString();
                if(resp.indexOf("*ERROR*")!=-1){
                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigEditor.this,"ERROR", resp);
                }
            } else {
                if(bindingdoc!=null){
                    first = bindingdoc.getFirstChild();
                    list = first.getChildNodes();
                    size = list.getLength();
                    if(first!=null){
                        for(int i=size-1;i>=0;i--){
                            first.removeChild(list.item(i));
                        }
                    }
                } else {
                    DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
                    DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
                    bindingdoc = documentBuilder.newDocument();
                    first = bindingdoc.createElement("root");
                    bindingdoc.appendChild(first);
                }
                
//                 Enumeration e = ((DefaultMutableTreeNode)root.getFirstChild()).preorderEnumeration();
                Enumeration e = root.preorderEnumeration();
                Element binding = null;
                while(e.hasMoreElements()){
                    DefaultMutableTreeNode node = (DefaultMutableTreeNode)e.nextElement();
                    if(node.getLevel()==1){
                        binding = bindingdoc.createElement("binding");
                        first.appendChild(binding);
                        Element el = bindingdoc.createElement("name");
                        binding.appendChild(el);
                        el.appendChild(bindingdoc.createTextNode(node.toString()));
                        continue;
                    }
                    if(node.getUserObject() instanceof MyFolder){
                        MyFolder folder = (MyFolder)node.getUserObject();
                        if(folder.getSut()!=null&&!folder.getSut().equals("")){
                            TreePath tp =  new TreePath(node.getPath());
                            size = tp.getPathCount();
                            StringBuilder sb = new StringBuilder();
                            DefaultMutableTreeNode temp;
                            for(int i=2;i<size-1;i++){
                                sb.append(((MyFolder)((DefaultMutableTreeNode)tp.getPathComponent(i)).getUserObject()).getNode().getNodeValue());
                                sb.append("/");                            
                            }
                            sb.append(folder.getNode().getNodeValue());
                            String path = sb.toString();
                            String sut = folder.getSut();
                            Element bind = bindingdoc.createElement("bind");
                            bind.setAttribute("config", path);
                            bind.setAttribute("sut", sut);
                            binding.appendChild(bind);
                        }
                    }
                }
                
                TransformerFactory transformerFactory = TransformerFactory.newInstance();
                Transformer transformer = transformerFactory.newTransformer();
                transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
                transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
                DOMSource source = new DOMSource(bindingdoc);
                StringWriter writer = new StringWriter();
                StreamResult result = new StreamResult(writer);
                transformer.transform(source, result);
                
                
                String content =  writer.toString();
                content = DatatypeConverter.printBase64Binary(content.getBytes());
                String resp = RunnerRepository.getRPCClient().execute("writeFile", new Object[]{"~/twister/config/bindings.xml",content}).toString();
                if(resp.indexOf("*ERROR*")!=-1){
                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigEditor.this,"ERROR", resp);
                }
            }
        }
    }
        catch(Exception e){
            System.out.println("Could not save binding for:"+remotelocation);
            e.printStackTrace();
        }
    }
    
    
    private DefaultMutableTreeNode findInNode(DefaultMutableTreeNode node, String name){
        if(node==null)return null;
        int nr = node.getChildCount();
        for(int i=0;i<nr;i++){
            if(((DefaultMutableTreeNode)node.getChildAt(i)).getUserObject() instanceof MyParam)continue;
            if(((MyFolder)((DefaultMutableTreeNode)node.getChildAt(i)).getUserObject()).getNode().getNodeValue().toString().equalsIgnoreCase(name)){
                return (DefaultMutableTreeNode)node.getChildAt(i);
            }
        }
        return null;
    }
    
    
    
//     public void setTree(JTree tree){
//         jScrollPane1.setViewportView(tree);
//     }
    
    public void setConfigTree(ConfigTree cfgtree){
        this.cfgtree = cfgtree;
    }
    
    public void saveAs(){
        final JTextField tf = new JTextField();
        try{tf.setText(((DefaultMutableTreeNode)cfgtree.tree.getModel().
                                                getRoot()).getFirstChild().toString());
        }catch(Exception e){
            e.printStackTrace();
        }
        AbstractAction action = new AbstractAction(){
            public void actionPerformed(ActionEvent ev){
                remotelocation = tf.getText();
                writeXML();
                lastsave = true;
            }
        };
        new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,this,true).setAction(action);
    }
    
    public void save(){
        if(editable&&currentfile!=null)writeXML();
        saveBinding();
        lastsave = true;
    }
    
    public void setRemoteLocation(String remotelocation){
        this.remotelocation = remotelocation;
    }
    
    private void newConfigFile(){
        this.remotelocation = null;
        String user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, this,
                                                    "File Name", "Please enter file name");
        if(!user.equals("NULL")){
            try{File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+
                                    "Twister"+RunnerRepository.getBar()+"XML"+
                                    RunnerRepository.getBar()+user);
                DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
                DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
                Document document = documentBuilder.newDocument();
                TransformerFactory transformerFactory = TransformerFactory.newInstance();
                Transformer transformer = transformerFactory.newTransformer();
                transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
                DOMSource source = new DOMSource(document);
                Element root = document.createElement("root");
                document.appendChild(root);   
                Result result = new StreamResult(file);
                transformer.transform(source, result);
                parseDocument(file);
            } catch(Exception e){
                System.out.println("Could not create new file");
                e.printStackTrace();
            }
        }
    }
    

    public void setDescription(final Node name, final Node desc, 
                               final Node type, final Node value,
                               final DefaultMutableTreeNode treenode, boolean editable){
                                   
        tvalue.setEnabled(editable);                 
        tdescription.setEnabled(editable);
        ttype.setEnabled(editable); 
        tname.setEnabled(editable); 
        
        for(KeyListener k:tvalue.getKeyListeners()){
            tvalue.removeKeyListener(k);
        }
        for(KeyListener listener:tdescription.getKeyListeners()){
            tdescription.removeKeyListener(listener);
        }
        for(ItemListener l:ttype.getItemListeners()){
            ttype.removeItemListener(l);
        }
        if(type!=null){
            try{String str = type.getNodeValue();
                if(str.equals("decimal")){
                    ttype.setSelectedIndex(0);
                    docum.setType('d');
                } else if(str.equals("hex")){
                    ttype.setSelectedIndex(1);
                    docum.setType('h');
                } else if(str.equals("octet")){
                    ttype.setSelectedIndex(2);
                    docum.setType('b');
                } else {
                    ttype.setSelectedIndex(3);
                    docum.setType('a');
                }
            } catch(Exception e){}
            if(editable){
                ttype.addItemListener(new ItemListener(){
                    public void itemStateChanged(ItemEvent ev){
                        if(ev.getStateChange()==ItemEvent.SELECTED){
                            String selected = ttype.getSelectedItem().toString();
                            docum.setType('a');
                            tvalue.setText("");
                            if(selected.equals("decimal")){
                                try{docum.setType('d');
                                    type.setNodeValue("decimal");
                                } catch (Exception e){e.printStackTrace();}
                            } else if (selected.equals("hex")){
                                try{type.setNodeValue("hex");
                                    docum.setType('h');
                                    tvalue.setText("0x");
                                } catch (Exception e){e.printStackTrace();}
                            } else if (selected.equals("octet")){
                                try{type.setNodeValue("octet");
                                    docum.setType('b');
                                } catch (Exception e){e.printStackTrace();}
                            } else {
                                try{type.setNodeValue("string");
                                    docum.setType('a');
                                } catch (Exception e){e.printStackTrace();}
                            }
                            value.setNodeValue(tvalue.getText());
                            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                        }
                    }
                });
            }
        }
        try{tname.setText(name.getNodeValue());}
        catch(Exception e){tname.setText("");}
        focusadapter.setNode(name);
        focusadapter.setTreeNode(treenode);
        if(value!=null){
            try{tvalue.setText(value.getNodeValue());}
            catch(Exception e){tvalue.setText("");}
            if(editable){
                tvalue.addKeyListener(new KeyAdapter(){
                    public void keyReleased(KeyEvent ev){
                        value.setNodeValue(tvalue.getText());
                        ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                    }
                });
            }
        }else{
            tvalue.setText("");
        }
        if(desc!=null){
            try{tdescription.setText(desc.getNodeValue());}
            catch(Exception e){tdescription.setText("");}
            if(editable){
                tdescription.addKeyListener(new KeyAdapter(){
                    public void keyReleased(KeyEvent ev){
                        String dsc = tdescription.getText();
                        if(dsc.length()>60){
                            dsc = dsc.substring(0,60);
                            tdescription.setText(dsc);
                        }
                        desc.setNodeValue(dsc);
                    }
                });
            }
        }
    }
    
    public void addParam(){
        TreePath tp = tree.getSelectionPath();
        DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
        MyFolder folder = (MyFolder)treenode.getUserObject();
        appendParam(treenode,folder);
        lastsave = false;
    }
    
    public void addConf(){
        TreePath tp = tree.getSelectionPath();
        if(tp==null){
            addFolder();
        } else{
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
            MyFolder folder = (MyFolder)treenode.getUserObject();
            appendFolder(treenode,folder);
        }
        lastsave = false;
    }
    
    public void deleteMultiple(){
        TreePath []tps = tree.getSelectionPaths();
        for(TreePath pth:tps){
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)pth.getLastPathComponent();
            Object myObj = treenode.getUserObject();
            if( myObj instanceof MyFolder){
                try{removeFolder((MyFolder)myObj, treenode,false);}
                catch(Exception e){e.printStackTrace();}
            } else if(myObj instanceof MyParam){
                try{removeParam((MyParam)myObj, treenode,false);}
                catch(Exception e){e.printStackTrace();}
            }
        }
        remove.setEnabled(false);
        addconf.setEnabled(true);
        addparam.setEnabled(false);
        setDescription(null, null, null, null, null, false);
        lastsave = false;
    }

    public void showNewFolderPopUp(MouseEvent ev){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Add Component");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addFolder();}});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    public void addFolder(){
        String resp = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    panel, "Name", "Config name: ");
        if(resp!=null){
            if(resp.equals("")){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name must not be null");
                return;
            }
            for(int i=0;i<root.getChildCount();i++){
                Object node = ((DefaultMutableTreeNode)root.getChildAt(i)).getUserObject();
                if(node.getClass() == MyFolder.class){
                    if(((MyFolder)node).toString().equals(resp)){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name already exists");
                        return;
                    }
                }
            }
            try{
                Element rootElement = doc.createElement("folder");
                doc.getFirstChild().appendChild(rootElement);
                Element fname = doc.createElement("fname");
                rootElement.appendChild(fname);  
                Node node = doc.createTextNode(resp);
                fname.appendChild(node);
                MyFolder folder = new MyFolder(node);
                
                fname = doc.createElement("fdesc");
                rootElement.appendChild(fname);  
                node = doc.createTextNode("");
                fname.appendChild(node);
                folder.setDesc(node);
                
                DefaultMutableTreeNode temp = new DefaultMutableTreeNode(folder,true);
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, root,root.getChildCount());
                if(root.getChildCount()==1){
                    ((DefaultTreeModel)tree.getModel()).reload();
                }
                
            } catch(Exception e){
                e.printStackTrace();
            }
        }
        lastsave = false;
    }
    
    /*
     * popup user on Node
     * right click
     */
    public void showParamPopUp(final DefaultMutableTreeNode treenode,MouseEvent ev,final MyParam node){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Change Parameter");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                changeParam(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Remove Parameter");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(acceptRemove())removeParam(node,treenode,true);}});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    private boolean acceptRemove(){
        int r = (Integer)CustomDialog.showDialog(new JLabel("Remove element ?"),
                                JOptionPane.QUESTION_MESSAGE, 
                                JOptionPane.OK_CANCEL_OPTION, this, "Remove", null);
        if(r == JOptionPane.OK_OPTION){
            return true;
        }
        return false;
    }
    
    /*
     * remove parameter
     */
    public void removeParam(MyParam node,DefaultMutableTreeNode treenode,boolean refresh){
        ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
        Node child = node.getValue().getParentNode().getParentNode();
        child.getParentNode().removeChild(child);
        if(refresh){
//             writeXML();
//             uploadFile();
            remove.setEnabled(false);
            addconf.setEnabled(true);
            addparam.setEnabled(false);
            setDescription(null, null, null, null, null,false);
        }
        lastsave = false;
    }
    
    /*
     * change parameter node
     */
    public void changeParam(DefaultMutableTreeNode treenode,MyParam node){  
        final JTextField name = new JTextField(); 
        name.addAncestorListener(new AncestorListener() {
            
            @Override
            public void ancestorRemoved(AncestorEvent arg0) {}
            
            @Override
            public void ancestorMoved(AncestorEvent arg0) {}
            
            @Override
            public void ancestorAdded(AncestorEvent arg0) {
                name.requestFocusInWindow();
            }
        });
        try{name.setText(node.getName().getNodeValue());}
        catch(Exception e){}
        final JTextField value = new JTextField();
        final JComboBox combo = new JComboBox(new String[]{"decimal","hex","octet","string"});
        final IntegerRangeDocument docum = new IntegerRangeDocument(0,255,'d');
        try{String type = node.getType().getNodeValue();
            if(type.equals("decimal")){
                combo.setSelectedIndex(0);
            } else if(type.equals("hex")){
                combo.setSelectedIndex(1);
                docum.setType('h');
            } else if(type.equals("octet")){
                combo.setSelectedIndex(2);
                docum.setType('b');
            } else {
                combo.setSelectedIndex(3);
                docum.setType('a');
            }
        } catch(Exception e){}
        value.setDocument(docum);
        combo.addItemListener(new ItemListener(){
            public void itemStateChanged(ItemEvent ev){
                if(ev.getStateChange()==ItemEvent.SELECTED){
                    String selected = combo.getSelectedItem().toString();
                    docum.setType('a');
                    value.setText("");
                    if(selected.equals("decimal")){
                        try{docum.setType('d');
                        } catch (Exception e){e.printStackTrace();}
                    } else if (selected.equals("hex")){
                        try{docum.setType('a');
                            value.setText("0x");
                            docum.setType('h');
                        } catch (Exception e){e.printStackTrace();}
                    } else if (selected.equals("octet")){
                        try{
                            docum.setType('b');
                        } catch (Exception e){e.printStackTrace();}
                    } else {
                        try{
                            docum.setType('a');
                        } catch (Exception e){e.printStackTrace();}
                    }
                    value.setText("");
                }
            }
        });
        try{value.setText(node.getValue().getNodeValue());}
        catch(Exception e){}
        JPanel p = getPropPanel(name,value,combo);
        int r = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                                                JOptionPane.OK_CANCEL_OPTION, 
                                                panel, "Property: value",null);
        if(r == JOptionPane.OK_OPTION){
            if(name.getText().equals("")){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name must not be null");
                return;
            }
            //check if name already exists
            for(int i=0;i<treenode.getParent().getChildCount();i++){
                Object ob = ((DefaultMutableTreeNode)treenode.getParent().getChildAt(i)).getUserObject();
                if(ob.getClass() == MyParam.class && ob!=node){
                    if(((MyParam)ob).getName().getNodeValue().equals(name.getText())){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name already exists");
                        return;
                    }
                }
            }
            node.getName().setNodeValue(name.getText());
            node.getValue().setNodeValue(value.getText());
            node.getType().setNodeValue(combo.getSelectedItem().toString());
            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
//             writeXML();
//             uploadFile();
            setDescription(node.getName(),node.getDesc(),node.getType(),node.getValue(),treenode,false);
            lastsave = true;
        }
    }

    /*
     * name value panel created
     * for adding props
     */        
    public JPanel getPropPanel(JTextField name, JTextField value, JComboBox combo){
        JPanel p = new JPanel();
        p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
        JLabel jLabel3 = new JLabel("Name: ");
        JPanel jPanel1 = new JPanel();
        jPanel1.setLayout(new java.awt.BorderLayout());
        jPanel1.add(jLabel3, BorderLayout.CENTER);
        p.add(jPanel1);
        p.add(name);
        if(value!=null){
            JPanel jPanel2 = new JPanel();
            JLabel jLabel4 = new JLabel("Value: ");
            jPanel2.setLayout(new BorderLayout());
            jPanel2.add(jLabel4, BorderLayout.CENTER);
            p.add(jPanel2);
            p.add(value);
        }
        if(combo!=null){
             JLabel jLabel5 = new JLabel("Type: ");
            JPanel jPanel3 = new JPanel();
            jPanel3.setLayout(new java.awt.BorderLayout());
            jPanel3.add(jLabel5, BorderLayout.CENTER);
            p.add(jPanel3);
            p.add(combo);
        }
        return p;}
    
    /*
     * popup user on Node
     * right click
     */
    public void showFolderPopUp(final DefaultMutableTreeNode treenode,MouseEvent ev,final MyFolder node){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Rename Config");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                renameFolder(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Add Config");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                appendFolder(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Add Parameter");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                appendParam(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Remove Config");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(acceptRemove())removeFolder(node,treenode,true);}});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    public void renameFolder(DefaultMutableTreeNode treenode, MyFolder parent){
        final JTextField name = new JTextField();  
        name.addAncestorListener(new AncestorListener() {
            
            @Override
            public void ancestorRemoved(AncestorEvent arg0) {}
            
            @Override
            public void ancestorMoved(AncestorEvent arg0) {}
            
            @Override
            public void ancestorAdded(AncestorEvent arg0) {
                name.requestFocusInWindow();
            }
        });
        name.setText(parent.toString());
        JPanel p = getPropPanel(name,null,null);
        int r = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                                                JOptionPane.OK_CANCEL_OPTION, 
                                                panel, "Config name",null);
        if(r == JOptionPane.OK_OPTION){
            if(name.getText().equals("")){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name must not be null");
                return;
            }
            
            //check if name already exists
            for(int i=0;i<treenode.getParent().getChildCount();i++){
                Object node = ((DefaultMutableTreeNode)treenode.getParent().getChildAt(i)).getUserObject();
                if(node.getClass() == MyFolder.class && node!=parent){
                    if(((MyFolder)node).toString().equals(name.getText())){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name already exists");
                        return;
                    }
                }
            }
            parent.getNode().setNodeValue(name.getText());
            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
//             writeXML();
//             uploadFile();
            setDescription(parent.getNode(),parent.getDesc(),null,null,treenode,false);
            lastsave = true;
        }
    }
        
    /*
     * create and append new node 
     * to this parent node
     */
    public void appendParam(DefaultMutableTreeNode treenode, MyFolder parent){
        
        final JTextField name = new JTextField();
        name.addAncestorListener(new AncestorListener() {
            public void ancestorRemoved(AncestorEvent arg0) {}
            public void ancestorMoved(AncestorEvent arg0) {}
            public void ancestorAdded(AncestorEvent arg0) {
                name.requestFocusInWindow();
            }
        });
        
        final JTextField value = new JTextField();
        final JComboBox combo = new JComboBox(new String[]{"decimal","hex","octet","string"});
        final IntegerRangeDocument docum = new IntegerRangeDocument(0,255,'d');
        value.setDocument(docum);
        combo.addItemListener(new ItemListener(){
            public void itemStateChanged(ItemEvent ev){
                if(ev.getStateChange()==ItemEvent.SELECTED){
                    String selected = combo.getSelectedItem().toString();
                    docum.setType('a');
                    value.setText("");
                    if(selected.equals("decimal")){
                        try{
                            docum.setType('d');
                        } catch (Exception e){e.printStackTrace();}
                    } else if (selected.equals("hex")){
                        try{docum.setType('a');
                            value.setText("0x");
                            docum.setType('h');
                        } catch (Exception e){e.printStackTrace();}
                    } else if (selected.equals("octet")){
                        try{
                            docum.setType('b');
                        } catch (Exception e){e.printStackTrace();}
                    } else {
                        try{
                            docum.setType('a');
                        } catch (Exception e){e.printStackTrace();}
                    }
                    value.setText("");
                }
            }
        });
        
        JPanel p = getPropPanel(name,value,combo);
        int r = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                                                JOptionPane.OK_CANCEL_OPTION, 
                                                panel, "Property: value",null);
        if(r == JOptionPane.OK_OPTION ){
            if(name.getText().equals("")){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name must not be null");
                return;
            }
            for(int i=0;i<treenode.getChildCount();i++){
                
                Object node = ((DefaultMutableTreeNode)treenode.getChildAt(i)).getUserObject();
                
                if(node.getClass() == MyParam.class){
                    if(((MyParam)node).getName().getNodeValue().equals(name.getText())){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name already exists");
                        return;
                    }
                }
            }
            MyParam param = new MyParam();
            
            Element rootElement = doc.createElement("param");
            parent.getNode().getParentNode().getParentNode().appendChild(rootElement);
            
            Node refs = null;
            try{refs = parent.getNode().getParentNode().getParentNode().
                       getFirstChild().getNextSibling().getNextSibling().getNextSibling();}
            catch(Exception e){refs=null;}
            if(refs==null){
                parent.getNode().getParentNode().getParentNode().appendChild(rootElement);
            } else {
                parent.getNode().getParentNode().getParentNode().insertBefore(rootElement, refs);
            }
            
            Element tname = doc.createElement("name");
            rootElement.appendChild(tname);  
            Node node = doc.createTextNode(name.getText());
            param.setName(node);
            tname.appendChild(node);
            
            Element tvalue = doc.createElement("value");
            rootElement.appendChild(tvalue);  
            node = doc.createTextNode(value.getText());
            param.setValue(node);
            tvalue.appendChild(node);
            
            Element tdesc = doc.createElement("desc");
            rootElement.appendChild(tdesc);  
            node = doc.createTextNode("");
            param.setDesc(node);
            tdesc.appendChild(node);
            
            Element ttype = doc.createElement("type");
            rootElement.appendChild(ttype);  
            node = doc.createTextNode(combo.getSelectedItem().toString());
            param.setType(node);
            ttype.appendChild(node);
            
            DefaultMutableTreeNode temp = new DefaultMutableTreeNode(param,true);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treenode,0);
            lastsave = false;
            
//             writeXML();
//             uploadFile();
        }
    }
    
    /*
     * create and append new node 
     * to this parent node
     */
    public void appendFolder(DefaultMutableTreeNode treenode, MyFolder parent){
        String resp = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    panel, "Name", "Config name: ");
        //check if name already exists
        if(resp!=null){
            if(resp.equals("")){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name must not be null");
                return;
            }
            for(int i=0;i<treenode.getChildCount();i++){
                
                Object node = ((DefaultMutableTreeNode)treenode.getChildAt(i)).getUserObject();
                
                if(node.getClass() == MyFolder.class){
                    if(((MyFolder)node).toString().equals(resp)){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,this,
                                                  "Warning", "Name already exists");
                        return;
                    }
                }
            }
            Element rootElement = doc.createElement("folder");
            parent.getNode().getParentNode().getParentNode().appendChild(rootElement);
            
            Element fname = doc.createElement("fname");
            rootElement.appendChild(fname);  
            Node node = doc.createTextNode(resp);
            fname.appendChild(node);
            
            MyFolder folder = new MyFolder(node);
            
            Element fdesc = doc.createElement("fdesc");
            rootElement.appendChild(fdesc);
            node = doc.createTextNode("");
            fdesc.appendChild(node);
            folder.setDesc(node);
            
            DefaultMutableTreeNode temp = new DefaultMutableTreeNode(folder,true);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treenode,treenode.getChildCount());
            lastsave = false;
        }
    }
    
    /*
     * remove node
     */
    public void removeFolder(MyFolder node,DefaultMutableTreeNode treenode, boolean refresh){
        ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
        Node child = node.getNode().getParentNode().getParentNode();
        child.getParentNode().removeChild(child);
//         if(refresh){
// //             writeXML();
// //             uploadFile();
//         }
        remove.setEnabled(false);
        addconf.setEnabled(true);
        addparam.setEnabled(false);
        setDescription(null, null, null, null, null,true);
        lastsave = false;
    }
    
//     public File getGlobalsFile(){
//         File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+
//                              "Twister"+RunnerRepository.getBar()+"config"+
//                              RunnerRepository.getBar()+"globals.xml");
//         try{String content = RunnerRepository.getRemoteFileContent(RunnerRepository.GLOBALSREMOTEFILE);
//             try{BufferedWriter writer = new BufferedWriter(new FileWriter(file));
//                 writer.write(content);
//                 writer.close();
//             } catch(Exception e){
//                 e.printStackTrace();
//             }            
//         }
//         catch(Exception e){
//             e.printStackTrace();
//             System.out.println("Could not get :"+
//                                 RunnerRepository.GLOBALSREMOTEFILE+" as globals parameter file");
//             return file;
//         }
//         return file;
//     }
        
    public void buildTree(){     
        try{
            setDescription(null,null,null,null,null,false);
            tree.setSelectionPath(null);
            remove.setEnabled(false);
            addconf.setEnabled(true);
            addparam.setEnabled(false);
            xpath = XPathFactory.newInstance().newXPath();
            XPathExpression expr1 = xpath.compile("//root/folder");
            NodeList nodes = (NodeList)expr1.evaluate(doc, XPathConstants.NODESET);
            root.removeAllChildren();
            for(int i=0;i<nodes.getLength();i++){
                parseFolder(nodes.item(i),root);
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        ((DefaultTreeModel)tree.getModel()).reload();
    }
    
    public void parseFolder(Node node,DefaultMutableTreeNode parent){
        try{
            Node n = ((Element)node).getElementsByTagName("fname").item(0);
            MyFolder fname = new MyFolder(n.getFirstChild());
            n = ((Element)node).getElementsByTagName("fdesc").item(0);
            try{
                if(n.getChildNodes().getLength()>0){
                    fname.setDesc(n.getFirstChild()); 
                } else {
                    Node tn = doc.createTextNode("");
                    n.appendChild(tn);
                    fname.setDesc(tn);
                }
            } catch (Exception e){
                e.printStackTrace();
            }
            DefaultMutableTreeNode temp = new DefaultMutableTreeNode(fname,true);
            parent.add(temp);
            XPathExpression expr1 = xpath.compile("param");
            NodeList nodes = (NodeList)expr1.evaluate(node, XPathConstants.NODESET);
            for(int i=0;i<nodes.getLength();i++){
                MyParam param = new MyParam();
                n = ((Element)nodes.item(i)).getElementsByTagName("name").item(0);
                param.setName(n.getFirstChild());
                n = ((Element)nodes.item(i)).getElementsByTagName("value").item(0);
                if(n.getChildNodes().getLength()==0){
                    Node tn = doc.createTextNode("");
                    ((Element)nodes.item(i)).getElementsByTagName("value").item(0).appendChild(tn);
                    param.setValue(tn);
                } else {
                    param.setValue(n.getFirstChild());
                }
                temp.add(new DefaultMutableTreeNode(param,true));
                
                n = ((Element)nodes.item(i)).getElementsByTagName("desc").item(0);
                if(n.getFirstChild()!=null){
                    param.setDesc(n.getFirstChild());
                } else {
                    Node tn = doc.createTextNode("");
                    n.appendChild(tn);
                    param.setDesc(tn);
                }
                
                n = ((Element)nodes.item(i)).getElementsByTagName("type").item(0);
                if(n.getFirstChild()!=null){
                    param.setType(n.getFirstChild());
                } else {
                    Node tn = doc.createTextNode("");
                    n.appendChild(tn);
                    param.setType(tn);
                }
            }
            expr1 = xpath.compile("folder");
            nodes = (NodeList)expr1.evaluate(node, XPathConstants.NODESET);
            for(int i=0;i<nodes.getLength();i++){
                parseFolder(nodes.item(i),temp);
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    public void writeXML(){
        try{
            Writer outWriter = new StringWriter();
            StreamResult result = new StreamResult( outWriter );
            DOMSource source = new DOMSource(doc);                    
            //Result result = new StreamResult(file);
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            transformer.transform(source, result);
            StringBuffer sb = ((StringWriter)outWriter).getBuffer();
            String content =  sb.toString();
            content = DatatypeConverter.printBase64Binary(content.getBytes());
            String resp = RunnerRepository.getRPCClient().execute("saveConfigFile", new Object[]{remotelocation,content}).toString();
            if(resp.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigEditor.this,"ERROR", resp);
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    public void reinitialize(){
        root.removeAllChildren();
        ((DefaultTreeModel)tree.getModel()).reload();
        currentfile = null;
        setDescription(null,null,null,null,null,false);
        tree.setSelectionPath(null);
        remove.setEnabled(false);
        addconf.setEnabled(false);
        addparam.setEnabled(false);
        displayname.setText("Configuration file:");
//         saveas.setEnabled(false);
    }
    
    
//     private void uploadFile(){
//         try{StringBuilder path = new StringBuilder();
//             String[] globalsremote = RunnerRepository.GLOBALSREMOTEFILE.split("/");
//             String filename = globalsremote[globalsremote.length-1];
//             globalsremote[globalsremote.length-1]="";
//             for(String s:globalsremote){
//                 path.append("/");
//                 path.append(s);
//             }
//             path.delete(0, 1);
//             String location = path.toString();
//             FileInputStream in = new FileInputStream(globalsfile);
//             try{
//                 while(!finished){
//                     try{Thread.sleep(100);}
//                     catch(Exception e){e.printStackTrace();}
//                 }
//                 finished = false;
//                 ch.cd(location);
//                 ch.put(in, filename);
//                 in.close();
//                 finished = true;}
//             catch(Exception e){
//                 e.printStackTrace();
//                 finished = true;
//             }
//         } catch (Exception e){
//             e.printStackTrace();
//         }
//     }
    
     public void disconnect(){
        ch.disconnect();
        session.disconnect();
    }
    
    /*
     * initialize SFTP connection used
     * for plugins and configuration files transfer
     */
    public void initSftp(){
        try{
            JSch jsch = new JSch();
            session = jsch.getSession(RunnerRepository.user, RunnerRepository.host, 22);
            session.setPassword(RunnerRepository.password);
            Properties config = new Properties();
            config.put("StrictHostKeyChecking", "no");
            session.setConfig(config);
            session.connect();
            Channel channel = session.openChannel("sftp");
            channel.connect();
            ch = (ChannelSftp)channel;
        } catch (Exception e){
            System.out.println("ERROR: Could not initialize SFTP for plugins");
            e.printStackTrace();
        }
    }
    
    
    class MyFocusAdapter extends FocusAdapter{
        private Node name;
        private DefaultMutableTreeNode treenode;
        
        public void setNode(Node name){
            this.name = name;
        }
        
        public void setTreeNode(DefaultMutableTreeNode treenode){
            this.treenode = treenode;
        }
        
        public void focusLost(FocusEvent ev){
            if(tname.getText().equals("")){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,ConfigEditor.this,
                                              "Warning", "Name must not be empty");
                
                tree.setSelectionPath(new TreePath(treenode.getPath()));
                tname.setText(name.getNodeValue());
                tname.requestFocusInWindow();
                tname.requestFocus();
            } else {
                name.setNodeValue(tname.getText());
                ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
            }
        }
    }
    
    class IntegerRangeDocument extends PlainDocument {
        private int minimum, maximum;
        private int currentValue = 0;
        private char type;//b-byte, a-any, h-hex, d-decimal
      
    
        public IntegerRangeDocument(int minimum, int maximum, char type) {
            this.type = type;
            this.minimum = minimum;
            this.maximum = maximum;
        }
      
        public void setType(char type){
            this.type = type;
        }
    
        public int getValue() {
            return currentValue;
        }
    
        public void insertString(int offset, String string, AttributeSet attributes)
        throws BadLocationException {
            if (string == null) {
                return;
            } else {
                String newValue;
                int length = getLength();
                if (length == 0) {
                    newValue = string;
                } else {
                    String currentContent = getText(0, length);
                    StringBuffer currentBuffer = new StringBuffer(currentContent);
                    currentBuffer.insert(offset, string);
                    newValue = currentBuffer.toString();
                }
                if(type=='a'){
                    super.insertString(offset, string, attributes);
                } else if(type=='b'){
                    try {
                        currentValue = checkInput(newValue);
                        super.insertString(offset, string, attributes);
                    } catch (Exception exception) {}
                } else if(type=='h'){
                    try {
                        if (newValue.matches("(0x){0,1}[0-9a-fA-F]{0,8}")) {
                            super.insertString(offset, string, attributes);
                        }
                    } catch (Exception exception) {exception.printStackTrace();}
                } else if(type=='d'){
                    try {
                        if (newValue.matches("\\d*\\.?\\d*")) {
                            super.insertString(offset, string, attributes);
                        }
                    } catch (Exception exception) {exception.printStackTrace();}
                }
            }
        }
    
        public void remove(int offset, int length) throws BadLocationException {
            int currentLength = getLength();
            String currentContent = getText(0, currentLength);
            String before = currentContent.substring(0, offset);
            String after = currentContent.substring(length + offset, currentLength);
            String newValue = before + after;
            if(type=='a'){
                super.remove(offset, length);
            }
            else if(type=='b'){
                try {
                    currentValue = checkInput(newValue);
                    super.remove(offset, length);
                } catch (Exception exception) {}
            } else if(type=='h'){
                try {
                    if (newValue.matches("(0x){0,1}[0-9a-fA-F]{0,8}")) {
                        super.remove(offset, length);
                    }
                } catch (Exception exception) {exception.printStackTrace();}
            } else if(type=='d'){
                try {
                    if (newValue.matches("\\d*\\.?\\d*")) {
                        super.remove(offset, length);
                    }
                } catch (Exception exception) {exception.printStackTrace();}
            }
        }
    
        public int checkInput(String proposedValue) throws NumberFormatException {
            int newValue = 0;
            if (proposedValue.length() > 0) {
                newValue = Integer.parseInt(proposedValue);
            }
            if ((minimum <= newValue) && (newValue <= maximum)) {
                return newValue;
            } else {
                throw new NumberFormatException();
            }
        }
    }
    
    class ImportTreeTransferHandler extends TransferHandler {
        DataFlavor nodesFlavor;  
        DataFlavor[] flavors = new DataFlavor[1];
       
        public ImportTreeTransferHandler() {  
            try {  
                String mimeType = DataFlavor.javaJVMLocalObjectMimeType +  
                                  ";class=\"" +  
                                  String.class.getName() +  
                                  "\"";  
                nodesFlavor = new DataFlavor(mimeType);  
                flavors[0] = nodesFlavor;  
            } catch(ClassNotFoundException e) {  
                System.out.println("ClassNotFound: " + e.getMessage());  
            }  
        }  
       
        public boolean canImport(TransferHandler.TransferSupport support) {  
            if(!editable&&currentfile!=null)return false;
            support.setShowDropLocation(true);
            if(!support.isDrop()) {  
                return false;  
            }  
            if(!support.isDataFlavorSupported(nodesFlavor)) {  
                return false;  
            }
            JTree.DropLocation dl = (JTree.DropLocation)support.getDropLocation(); 
            TreePath dest = dl.getPath();  
            if(dest==null)return false;
            DefaultMutableTreeNode target = (DefaultMutableTreeNode)dest.getLastPathComponent(); 
           
            if(!(target.getUserObject() instanceof MyFolder)){
                return false;
            } else {
                if(currentfile==null){
                    if(target.getLevel()<2)return false;
                    DefaultMutableTreeNode parent = (DefaultMutableTreeNode)target.getPath()[0];
                    int index = parent.getIndex((DefaultMutableTreeNode)target.getPath()[1]);
                    if(index==0)return true;
                    return false;
                }
                return true;
            }
        }
        
        public int getSourceActions(JComponent c) {  
            return COPY;  
        }  
       
        public boolean importData(TransferHandler.TransferSupport support) {
            try{
                if(!canImport(support)) {  
                    return false;  
                }
                try {  
                    Transferable t = support.getTransferable();
                    String transfer = (String)t.getTransferData(nodesFlavor);
                    String file = transfer.split(" - ")[0];
                    String sutpath = transfer.split(" - ")[1];
                    JTree.DropLocation dl = (JTree.DropLocation)support.getDropLocation();  
                    TreePath dest = dl.getPath();  
                    DefaultMutableTreeNode parent = (DefaultMutableTreeNode)dest.getLastPathComponent();
                    JTree tree = (JTree)support.getComponent();  
                    DefaultTreeModel model = ((DefaultTreeModel)tree.getModel());
                    ((MyFolder)parent.getUserObject()).setSut(file);
                    ((MyFolder)parent.getUserObject()).setSutPath(sutpath);
                    model.nodeChanged(parent);
                    lastsave = false;
                    return true;
                } catch(UnsupportedFlavorException ufe) {
                    System.out.println("UnsupportedFlavor: " + ufe.getMessage());
                } catch(java.io.IOException ioe) {
                    System.out.println("I/O error: " + ioe.getMessage());
                }
                return false;
                
//                 Node[] nodes = null;  
//                 try {  
//                     Transferable t = support.getTransferable();  
//                     nodes = (Node[])t.getTransferData(nodesFlavor);  
//                 } catch(UnsupportedFlavorException ufe) {  
//                     System.out.println("UnsupportedFlavor: " + ufe.getMessage());  
//                 } catch(java.io.IOException ioe) {  
//                     System.out.println("I/O error: " + ioe.getMessage());  
//                 }
//                 JTree.DropLocation dl = (JTree.DropLocation)support.getDropLocation();  
//                 TreePath dest = dl.getPath();  
//                 DefaultMutableTreeNode parent = (DefaultMutableTreeNode)dest.getLastPathComponent();
//                 JTree tree = (JTree)support.getComponent();  
//                 DefaultTreeModel model = ((DefaultTreeModel)tree.getModel());  
//                 if(parent.getChildCount()>1){
//                     for(int i=0;i<parent.getChildCount();i++){
//                         if(((DefaultMutableTreeNode)parent.getChildAt(i)).getUserObject() instanceof Node){
//                             model.removeNodeFromParent((DefaultMutableTreeNode)parent.getChildAt(i));
//                         }
//                     }
//                 }
//                 int index = parent.getChildCount();  
//                 for(int i = 0; i < nodes.length; i++){ 
//                     try{
//                         Comp comparent = (Comp)parent.getUserObject();
//                         HashMap <String,String>hm = new <String,String>HashMap();
//                         hm.put("_id", nodes[i].getID());
//                         String parentid="";
//                         if(((DefaultMutableTreeNode)parent.getParent()).getUserObject() instanceof Comp){
//                             parentid = ((Comp)((DefaultMutableTreeNode)parent.getParent()).getUserObject()).getID();
//                         } else {
//                             parentid = "/"+parent.getParent().toString();
//                         }
//                         String resp = client.execute("setSut", new Object[]{comparent.getName(),parentid,hm}).toString();
//                         if(resp.indexOf("ERROR")==-1){
//                             DefaultMutableTreeNode element = createChildren(nodes[i]);
//                             model.insertNodeInto(element, parent, index++);
//                         }
//                         else{
//                             CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SUTEditor.this,"ERROR", resp);
//                         }
//                         
//                     } catch (Exception e){
//                         e.printStackTrace();
//                     }
//                     
//                 } 
//                 return true; 
            } catch(Exception e){
                e.printStackTrace();
                return false;
            }
//             return true;
        } 
        
//         private DefaultMutableTreeNode createChildren(Node node){
//             DefaultMutableTreeNode parent = new DefaultMutableTreeNode(node);
//             
//             DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+node.getID(),false);
//             parent.add(temp);
//             
//             temp = new DefaultMutableTreeNode(node.getPath(),false);
//             parent.add(temp);
//             
//             return parent;
//         }
       
        public String toString() {  
            return getClass().getName();  
        }  
       
//         public class StringTransferable implements Transferable {  
//             String file;  
//             DataFlavor nodesFlavor;  
//             DataFlavor[] flavors = new DataFlavor[1];
//        
//             public StringTransferable(String file) {  
//                 this.file = file;  
//                 try {  
//                     String mimeType = DataFlavor.javaJVMLocalObjectMimeType +  
//                                       ";class=\"" +  
//                                       String.class.getName() +  
//                                       "\"";  
//                     nodesFlavor = new DataFlavor(mimeType);  
//                     flavors[0] = nodesFlavor;  
//                 } catch(ClassNotFoundException e) {  
//                     System.out.println("ClassNotFound: " + e.getMessage());  
//                 }  
//              }  
//        
//             public Object getTransferData(DataFlavor flavor)  
//                                      throws UnsupportedFlavorException {  
//                 if(!isDataFlavorSupported(flavor))  
//                     throw new UnsupportedFlavorException(flavor);  
//                 return file;  
//             }  
//        
//             public DataFlavor[] getTransferDataFlavors() {  
//                 return flavors;  
//             }  
//        
//             public boolean isDataFlavorSupported(DataFlavor flavor) {  
//                 return nodesFlavor.equals(flavor);  
//             }  
//         }  
    }
}