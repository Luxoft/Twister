/*
File: Globals.java ; This file is part of Twister.
Version: 2.003

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
import javax.swing.tree.DefaultMutableTreeNode;
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

public class Globals {
    private ChannelSftp ch ;
    public JScrollPane panel;
    public JPanel main, pdesc;
    private JTree tree;
    private XPath xpath;
    private Document doc;
    private DefaultMutableTreeNode root;
    private File globalsfile;
    private boolean finished = true;
    private JButton addconf,addparam,remove;
    private JLabel cname;
    private JTextArea tdescription;
    private JTextField tvalue, tname;
    private JComboBox ttype;
    private IntegerRangeDocument docum;
    private MyFocusAdapter focusadapter;
    
    public Globals(){
        initSftp();
        parseDocument();
        init();
        buildTree();
    }
    
    public void refresh(){
        ((DefaultMutableTreeNode)tree.getModel().getRoot()).removeAllChildren();
        parseDocument();
        buildTree();
    }
    
    public void parseDocument(){
        try{DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            globalsfile = getGlobalsFile();
            if(globalsfile==null || !globalsfile.exists()){
                System.out.println(Repository.GLOBALSREMOTEFILE+" could not be opened localy");
                return;
            }
            doc = db.parse(globalsfile);
            doc.getDocumentElement().normalize();  
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
                .addContainerGap())
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
                .addContainerGap())
        );
    }

    public void init(){
        root = new DefaultMutableTreeNode("root", true);
        tree = new JTree(root);
        tree.setRootVisible(false);
        tree.setCellRenderer(new CustomIconRenderer());
        panel = new JScrollPane(tree);
        main = new JPanel();
        panel = new JScrollPane(tree);
        JPanel buttonPanel = new JPanel();
        
        addconf = new JButton("Add Config");
        addparam = new JButton("Add Parameter");
        remove = new JButton("Remove");
        
        addconf.setBounds(0,5,120,20);
        buttonPanel.add(addconf);
        addconf.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addConf();
            }
        });
        
        addparam.setBounds(130,5,140,20);
        buttonPanel.add(addparam);
        addparam.setEnabled(false);
        addparam.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addParam();
            }
        });

        remove.setBounds(280,5,100,20);
        remove.setEnabled(false);
        buttonPanel.add(remove);
        remove.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(acceptRemove())deleteMultiple();
            }
        });
        
        initParamDesc();
        main.setLayout(new BorderLayout());
        main.add(panel,BorderLayout.CENTER);
        main.add(buttonPanel,BorderLayout.SOUTH);
        main.add(pdesc,BorderLayout.EAST);
        GroupLayout buttonPanelLayout = new GroupLayout(buttonPanel);
        buttonPanel.setLayout(buttonPanelLayout);
        buttonPanelLayout.setHorizontalGroup(
            buttonPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        buttonPanelLayout.setVerticalGroup(
            buttonPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGap(0, 50, Short.MAX_VALUE)
        );
        tree.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_DELETE){
                    if(acceptRemove())deleteMultiple();
                }
            }
        });

        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                if (tp != null){
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        tree.setSelectionPath(tp);
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyFolder){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            MyFolder folder = (MyFolder)treenode.getUserObject();
                            showFolderPopUp(treenode,ev,folder);
                            addconf.setEnabled(true);
                            addparam.setEnabled(true);
                            remove.setEnabled(true);
                            setDescription(folder.getNode(), folder.getDesc(),null,null,(DefaultMutableTreeNode)tp.getLastPathComponent());
                        }else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyParam){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            MyParam param = (MyParam)treenode.getUserObject();
                            showParamPopUp(treenode,ev,param);
                            remove.setEnabled(true);
                            addconf.setEnabled(false);
                            addparam.setEnabled(false);
                            setDescription(param.getName(),param.getDesc(),param.getType(),param.getValue(),(DefaultMutableTreeNode)tp.getLastPathComponent());
                        }
                    } else if(ev.getButton() == MouseEvent.BUTTON1){
                        if(tree.getSelectionPaths().length==1){
                            tp = tree.getSelectionPath();
                            if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyFolder){
                                remove.setEnabled(true);
                                addconf.setEnabled(true);
                                addparam.setEnabled(true);
                                MyFolder folder = (MyFolder)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject();
                                setDescription(folder.getNode(), folder.getDesc(),null,null,(DefaultMutableTreeNode)tp.getLastPathComponent());
                            }else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyParam){
                                remove.setEnabled(true);
                                addconf.setEnabled(false);
                                addparam.setEnabled(false);
                                MyParam param = (MyParam)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject();
                                setDescription(param.getName(),param.getDesc(),param.getType(),param.getValue(),(DefaultMutableTreeNode)tp.getLastPathComponent());
                            }
                        } else {
                            setDescription(null,null,null,null,null);
                            remove.setEnabled(true);
                            addconf.setEnabled(false);
                            addparam.setEnabled(false);
                        }
                    }
                } else {
                    setDescription(null,null,null,null,null);
                    tree.setSelectionPath(null);
                    remove.setEnabled(false);
                    addconf.setEnabled(true);
                    addparam.setEnabled(false);
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        showNewFolderPopUp(ev);
                    }
                }
            }
        }
        );
    }
    

    public void setDescription(final Node name, final Node desc, final Node type, final Node value,final DefaultMutableTreeNode treenode){
        ttype.setEnabled(!(type==null));
        tvalue.setEnabled(!(value==null));
        tname.setEnabled(!(name==null));
        tdescription.setEnabled(!(desc==null));
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
        }
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
                    writeXML();
                    uploadFile();
                }
            }
        });
        try{tname.setText(name.getNodeValue());}
        catch(Exception e){tname.setText("");}
        focusadapter.setNode(name);
        focusadapter.setTreeNode(treenode);
        try{tdescription.setText(desc.getNodeValue());}
        catch(Exception e){tdescription.setText("");}
        if(value!=null){
            try{tvalue.setText(value.getNodeValue());}
            catch(Exception e){tvalue.setText("");}
            tvalue.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    value.setNodeValue(tvalue.getText());
                    ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                    writeXML();
                    uploadFile();
                }
            });
        }else{
            tvalue.setText("");
        }
        if(desc!=null){
            tdescription.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    String dsc = tdescription.getText();
                    if(dsc.length()>60){
                        dsc = dsc.substring(0,60);
                        tdescription.setText(dsc);
                    }
                    desc.setNodeValue(dsc);
                    writeXML();
                    uploadFile();
                }
            });
        }
    }
    
    public void addParam(){
        TreePath tp = tree.getSelectionPath();
        DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
        MyFolder folder = (MyFolder)treenode.getUserObject();
        appendParam(treenode,folder);
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
        writeXML();
        uploadFile();
        setDescription(null, null, null, null, null);
    }

    public void showNewFolderPopUp(MouseEvent ev){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Add Config");
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
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                                                  "Warning", "Name must not be null");
                return;
            }
            for(int i=0;i<root.getChildCount();i++){
                
                Object node = ((DefaultMutableTreeNode)root.getChildAt(i)).getUserObject();
                
                if(node.getClass() == MyFolder.class){
                    if(((MyFolder)node).toString().equals(resp)){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
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
                writeXML();
                uploadFile();
                
            } catch(Exception e){
                e.printStackTrace();
            }
        }
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
                                JOptionPane.OK_CANCEL_OPTION, main, "Remove", null);
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
            writeXML();
            uploadFile();
            remove.setEnabled(false);
            addconf.setEnabled(true);
            addparam.setEnabled(false);
            setDescription(null, null, null, null, null);
        }
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
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                                                  "Warning", "Name must not be null");
                return;
            }
            //check if name already exists
            for(int i=0;i<treenode.getParent().getChildCount();i++){
                Object ob = ((DefaultMutableTreeNode)treenode.getParent().getChildAt(i)).getUserObject();
                if(ob.getClass() == MyParam.class && ob!=node){
                    if(((MyParam)ob).getName().getNodeValue().equals(name.getText())){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                                                  "Warning", "Name already exists");
                        return;
                    }
                }
            }
            node.getName().setNodeValue(name.getText());
            node.getValue().setNodeValue(value.getText());
            node.getType().setNodeValue(combo.getSelectedItem().toString());
            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
            writeXML();
            uploadFile();
            setDescription(node.getName(),node.getDesc(),node.getType(),node.getValue(),treenode);
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
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                                                  "Warning", "Name must not be null");
                return;
            }
            
            //check if name already exists
            for(int i=0;i<treenode.getParent().getChildCount();i++){
                Object node = ((DefaultMutableTreeNode)treenode.getParent().getChildAt(i)).getUserObject();
                if(node.getClass() == MyFolder.class && node!=parent){
                    if(((MyFolder)node).toString().equals(name.getText())){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                                                  "Warning", "Name already exists");
                        return;
                    }
                }
            }
            parent.getNode().setNodeValue(name.getText());
            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
            writeXML();
            uploadFile();
            setDescription(parent.getNode(),parent.getDesc(),null,null,treenode);
        }
    }
        
    /*
     * create and append new node 
     * to this parent node
     */
    public void appendParam(DefaultMutableTreeNode treenode, MyFolder parent){
        
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
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                                                  "Warning", "Name must not be null");
                return;
            }
            for(int i=0;i<treenode.getChildCount();i++){
                
                Object node = ((DefaultMutableTreeNode)treenode.getChildAt(i)).getUserObject();
                
                if(node.getClass() == MyParam.class){
                    if(((MyParam)node).getName().getNodeValue().equals(name.getText())){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
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
            
            writeXML();
            uploadFile();
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
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                                                  "Warning", "Name must not be null");
                return;
            }
            for(int i=0;i<treenode.getChildCount();i++){
                
                Object node = ((DefaultMutableTreeNode)treenode.getChildAt(i)).getUserObject();
                
                if(node.getClass() == MyFolder.class){
                    if(((MyFolder)node).toString().equals(resp)){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
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
            
            writeXML();
            uploadFile();
        }
    }
    
    /*
     * remove node
     */
    public void removeFolder(MyFolder node,DefaultMutableTreeNode treenode, boolean refresh){
        ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
        Node child = node.getNode().getParentNode().getParentNode();
        child.getParentNode().removeChild(child);
        if(refresh){
            writeXML();
            uploadFile();
        }
        remove.setEnabled(false);
        addconf.setEnabled(true);
        addparam.setEnabled(false);
        setDescription(null, null, null, null, null);
    }
    
    public File getGlobalsFile(){
        File file = new File(Repository.temp+Repository.getBar()+
                             "Twister"+Repository.getBar()+"config"+
                             Repository.getBar()+"globals.xml");
        try{String content = Repository.getRemoteFileContent(Repository.GLOBALSREMOTEFILE);
            try{BufferedWriter writer = new BufferedWriter(new FileWriter(file));
                writer.write(content);
                writer.close();
            } catch(Exception e){
                e.printStackTrace();
            }            
        }
        catch(Exception e){
            e.printStackTrace();
            System.out.println("Could not get :"+
                                Repository.GLOBALSREMOTEFILE+" as globals parameter file");
            return file;
        }
        return file;
    }
        
    public void buildTree(){     
        try{xpath = XPathFactory.newInstance().newXPath();
            XPathExpression expr1 = xpath.compile("//root/folder");
            NodeList nodes = (NodeList)expr1.evaluate(doc, XPathConstants.NODESET);
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
            if(n.getFirstChild()!=null){
                fname.setDesc(n.getFirstChild()); 
            } else {
                Node tn = doc.createTextNode("");
                n.appendChild(tn);
                fname.setDesc(tn);
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
        try{DOMSource source = new DOMSource(doc);                    
            Result result = new StreamResult(globalsfile);
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            transformer.transform(source, result);
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    private void uploadFile(){
        try{StringBuilder path = new StringBuilder();
            String[] globalsremote = Repository.GLOBALSREMOTEFILE.split("/");
            String filename = globalsremote[globalsremote.length-1];
            globalsremote[globalsremote.length-1]="";
            for(String s:globalsremote){
                path.append("/");
                path.append(s);
            }
            path.delete(0, 1);
            String location = path.toString();
            FileInputStream in = new FileInputStream(globalsfile);
            try{
                while(!finished){
                    try{Thread.sleep(100);}
                    catch(Exception e){e.printStackTrace();}
                }
                finished = false;
                ch.cd(location);
                ch.put(in, filename);
                in.close();
                finished = true;}
            catch(Exception e){
                e.printStackTrace();
                finished = true;
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    /*
     * initialize SFTP connection used
     * for plugins and configuration files transfer
     */
    public void initSftp(){
        try{
            JSch jsch = new JSch();
            Session session = jsch.getSession(Repository.user, Repository.host, 22);
            session.setPassword(Repository.password);
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
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                                              "Warning", "Name must not be empty");
                
                tree.setSelectionPath(new TreePath(treenode.getPath()));
                //tree.setSelectionPath(treenode.getPath());
                tname.setText(name.getNodeValue());
                tname.requestFocusInWindow();
                tname.requestFocus();
            } else {
                name.setNodeValue(tname.getText());
                ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                writeXML();
                uploadFile();
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
}