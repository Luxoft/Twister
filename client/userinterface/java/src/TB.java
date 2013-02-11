import javax.swing.JPanel;
import java.awt.Color;
import java.util.HashMap;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;
import java.util.Iterator;
import java.util.Set;
import javax.swing.JTree;
import javax.swing.JScrollPane;
import javax.swing.tree.TreeSelectionModel;
import javax.swing.BorderFactory;
import javax.swing.border.BevelBorder;
import javax.swing.GroupLayout;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;
import java.awt.event.MouseAdapter;
import java.awt.event.KeyAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import javax.swing.tree.TreePath;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import com.twister.CustomDialog;
import javax.swing.JOptionPane;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JButton;

public class TB extends JPanel{
    private XmlRpcClient client;
    private Node parent;
    private JTree tree;
    private DefaultMutableTreeNode root;
    private NodePanel optpan;

    public TB(){
        initializeRPC();
        initPanel();
        parent = new Node("1","/","parent",null);
        parent = getTB("/",null);
        buildTree(parent,root);
        ((DefaultTreeModel)tree.getModel()).reload();
    }

    public void initPanel(){
        root = new DefaultMutableTreeNode("root", true);
        tree = new JTree(root);
        tree.setCellRenderer(new CustomIconRenderer());
        optpan = new NodePanel(tree,client);
        tree.setDragEnabled(false);
        tree.setRootVisible(false);
        tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        
        
        JScrollPane jScrollPane1 = new JScrollPane();
        //tree = new javax.swing.JTree();
//         JPanel optpan = new javax.swing.JPanel();
//         JLabel name = new javax.swing.JLabel();
//         JLabel id = new javax.swing.JLabel();
//         JLabel path = new javax.swing.JLabel();
//         JTextField tname = new javax.swing.JTextField();
//         JTextField tid = new javax.swing.JTextField();
//         JTextField tpath = new javax.swing.JTextField();
//         JPanel jPanel1 = new javax.swing.JPanel();
//         JScrollPane jScrollPane2 = new javax.swing.JScrollPane();
//         JPanel proppanel = new javax.swing.JPanel();
//         JLabel jLabel1 = new javax.swing.JLabel();
//         JTextField jTextField1 = new javax.swing.JTextField();
//         JLabel jLabel2 = new javax.swing.JLabel();
//         JTextField jTextField2 = new javax.swing.JTextField();
//         JButton jButton1 = new javax.swing.JButton();

        tree.setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
        jScrollPane1.setViewportView(tree);
        
        //optpan.setBorder(javax.swing.BorderFactory.createBevelBorder(javax.swing.border.BevelBorder.RAISED));

//         name.setText("Name: ");
// 
//         id.setText("ID: ");
// 
//         path.setText("Path:");
// 
//         jPanel1.setBorder(javax.swing.BorderFactory.createTitledBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)), "Properties"));
// 
//         jScrollPane2.setBorder(null);
//         jScrollPane2.setPreferredSize(new java.awt.Dimension(300, 150));
// 
//         proppanel.setPreferredSize(new java.awt.Dimension(280, 150));
//         proppanel.setLayout(null);
// 
//         jLabel1.setText("Name");
//         proppanel.add(jLabel1);
//         jLabel1.setBounds(10, 14, 27, 14);
//         proppanel.add(jTextField1);
//         jTextField1.setBounds(41, 11, 95, 20);
// 
//         jLabel2.setText("Value:");
//         proppanel.add(jLabel2);
//         jLabel2.setBounds(146, 14, 30, 14);
//         proppanel.add(jTextField2);
//         jTextField2.setBounds(180, 11, 100, 20);
// 
//         jButton1.setText("Add");
//         proppanel.add(jButton1);
//         jButton1.setBounds(229, 37, 51, 23);
// 
//         jScrollPane2.setViewportView(proppanel);
// 
//         javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
//         jPanel1.setLayout(jPanel1Layout);
//         jPanel1Layout.setHorizontalGroup(
//             jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE)
//         );
//         jPanel1Layout.setVerticalGroup(
//             jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addComponent(jScrollPane2, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//         );

        


        javax.swing.GroupLayout layout = new GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 240, Short.MAX_VALUE)
                .addGap(18, 18, 18)
                .addComponent(optpan, GroupLayout.PREFERRED_SIZE, 390, GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.TRAILING)
                    .addComponent(optpan, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 444, Short.MAX_VALUE))
                .addContainerGap())
        );       
        
        
        
        
        
//         JScrollPane jScrollPane1 = new JScrollPane();
//         JPanel jPanel1 = new JPanel();
// 
//         tree.setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
//         jScrollPane1.setViewportView(tree);
// 
//         jPanel1.setBorder(BorderFactory.createBevelBorder(BevelBorder.RAISED));
// 
//         GroupLayout jPanel1Layout = new GroupLayout(jPanel1);
//         jPanel1.setLayout(jPanel1Layout);
//         jPanel1Layout.setHorizontalGroup(
//             jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGap(0, 350, Short.MAX_VALUE)
//         );
//         jPanel1Layout.setVerticalGroup(
//             jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGap(0, 0, Short.MAX_VALUE)
//         );
// 
//         GroupLayout layout = new GroupLayout(this);
//         this.setLayout(layout);
//         layout.setHorizontalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 396, Short.MAX_VALUE)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addComponent(jPanel1, GroupLayout.PREFERRED_SIZE, 
//                                 GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
//                 .addContainerGap())
//         );
//         layout.setVerticalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.TRAILING)
//                     .addComponent(jPanel1, GroupLayout.DEFAULT_SIZE,
//                                   GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                     .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 442, Short.MAX_VALUE))
//                 .addContainerGap())
//         );
        tree.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_DELETE){
                    TreePath tp = tree.getSelectionPath();
                    if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Node){
                        DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                        Node node = (Node)treenode.getUserObject();
                        removeNode(node,treenode);
                    }
                }
            }
        });
        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                if (tp != null){
                    tree.setSelectionPath(tp);
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Node){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            Node node = (Node)treenode.getUserObject();
                            showNodePopUp(treenode,ev,node);
                        }
                    } else{
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Node){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            Node node = (Node)treenode.getUserObject();
                            optpan.setParent(node,treenode);
                        }
                    }
                } else {
                    tree.setSelectionPath(null);
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        addRootNodePopUp(ev);
                    } 
                }}});
    }
    
    public JTree getTree(){
        return tree;
    }
    
    
    public void addRootNodePopUp(MouseEvent ev){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Add TestBed");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String resp = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    TB.this, "Name", "TestBed name: ");
                if(resp!=null&&!resp.equals("")){
                    try{
                        //String id, String path, String name
                        Node newnode = new Node(null,resp,resp,parent);
                        resp = client.execute("setResource", new Object[]{resp,"/",null}).toString();
                        newnode.setID(resp);
                        DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(newnode);
                        DefaultMutableTreeNode root = (DefaultMutableTreeNode)((DefaultTreeModel)tree.getModel()).getRoot();
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, root,root.getChildCount());
                        
                        DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+newnode.getID());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,treechild.getChildCount());
                        
                        
                        DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode("Path: "+newnode.getPath());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,treechild.getChildCount());
                        
                        
                        //((DefaultTreeModel)tree.getModel()).reload();
                    } catch (Exception e){
                        e.printStackTrace();
                    }
                }            
            }});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    /*
     * popup user on Node
     * right click
     */
    public void showNodePopUp(final DefaultMutableTreeNode treenode,MouseEvent ev,final Node node){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Add component");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                appendNode(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Remove");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeNode(node,treenode);}});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    /*
     * create and append new node 
     * to this parent node
     */
    public void appendNode(DefaultMutableTreeNode treenode, Node parent){
        String resp = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    this, "Name", "Component name: ");
        if(resp!=null&&!resp.equals("")){
            try{
                //String id, String path, String name
                Node newnode = new Node(null,parent.getPath()+"/"+resp,resp,parent);
                resp = client.execute("setResource", new Object[]{resp,parent.getID(),null}).toString();
                newnode.setID(resp);
                DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(newnode);
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode,treenode.getChildCount());
                
                DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+newnode.getID());
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,treechild.getChildCount());
                
                
                DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode("Path: "+newnode.getPath());
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,treechild.getChildCount());
                
                
                //((DefaultTreeModel)tree.getModel()).reload();
            } catch (Exception e){
                e.printStackTrace();
            }
        }
    }
    
    /*
     * remove node
     */
    public void removeNode(Node node,DefaultMutableTreeNode treenode){
        try{String s = client.execute("deleteResource", new Object[]{node.getID()}).toString();
            System.out.println("removing "+node.getID()+" "+s);
            if(s.equals("true")){
                Node parent = node.getParent();
                if(parent!=null)parent.removeChild(node.getID());
                ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
                optpan.setParent(null,null);
            }
        }
        catch(Exception e){e.printStackTrace();}
    }
    
    /*
     * print tree nodes name
     * starting from node
     */
    public void printTree(Node node){
        System.out.println("Name: "+node.getName());
        Iterator iter = node.getChildren().keySet().iterator();
        while(iter.hasNext()){
            String childid = iter.next().toString();
            printTree(node.getChild(childid));
        }
    }
    
    
    /*
     * build whole 
     * structure from scratch
     */
    public void buildTree(Node node, DefaultMutableTreeNode treenode){
        try{
            Iterator iter = node.getChildren().keySet().iterator();
            while(iter.hasNext()){
                String childid = iter.next().toString();
                
                Node child = getTB(childid,node);
                
                node.addChild(childid, child);
                DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(child);
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode,treenode.getChildCount());
                
                DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+child.getID());
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,treechild.getChildCount());
                
                
                DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode("Path: "+child.getPath());
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,treechild.getChildCount());
                
                buildTree(child,treechild);
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }

    /*
     * create a node based om am id
     * the node is created from the data 
     * received from server
     */
    public Node getTB(String id,Node parent){
        try{HashMap hash= (HashMap)client.execute("getResource", new Object[]{id});
            String path = hash.get("path").toString();
            String name = path.split("/")[path.split("/").length-1];
            Node node = new Node(id,path,name,parent);
            Object[] children = (Object[])hash.get("children");
            for(Object o:children){
                node.addChild(o.toString(), null);
            }
            HashMap meta = (HashMap)hash.get("meta");
            if(meta!=null&&meta.size()!=0){
                Set keys = meta.keySet();
                Iterator iter = keys.iterator();
                while(iter.hasNext()){
                    String n = iter.next().toString();
                    node.addProperty(n, meta.get(n).toString());
                }
            }
            return node;
        }catch(Exception e){
            e.printStackTrace();
            return null;
        }
    }

    /*
     * initialize RPC connection
     * based on host an port of 
     * resource allocator specified in config
     */
    public void initializeRPC(){
        try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
            configuration.setServerURL(new URL("http://"+Repository.host+
                                        ":"+Repository.getCentralEnginePort()+"/ra/"));
                                        
                                        //+Repository.getResourceAllocatorPort()));
            configuration.setEnabledForExtensions(true);
            client = new XmlRpcClient();
            client.setConfig(configuration);
            System.out.println("XMLRPC Client for testbed initialized: "+client);}
        catch(Exception e){System.out.println("Could not conect to "+
                            Repository.host+" :"+Repository.getCentralEnginePort()+"/ra/"+
                            "for RPC client initialization");}
    }
}