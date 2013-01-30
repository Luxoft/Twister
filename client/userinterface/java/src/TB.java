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

public class TB extends JPanel{
    private XmlRpcClient client;
    private Node parent;
    private JTree tree;
    private DefaultMutableTreeNode root;

    public TB(){
        initPanel();
        initializeRPC();
        parent = new Node("1","/","parent");
        parent = getTB("/");
        buildTree(parent,root);
        ((DefaultTreeModel)tree.getModel()).reload();
    }

    public void initPanel(){
        
        JScrollPane jScrollPane1 = new JScrollPane();
        root = new DefaultMutableTreeNode("root", true);
        tree = new JTree(root);
        tree.setDragEnabled(false);
        tree.setRootVisible(false);
        tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        JPanel jPanel1 = new JPanel();

        tree.setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
        jScrollPane1.setViewportView(tree);

        jPanel1.setBorder(BorderFactory.createBevelBorder(BevelBorder.RAISED));

        GroupLayout jPanel1Layout = new GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGap(0, 350, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );

        GroupLayout layout = new GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 396, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jPanel1, GroupLayout.PREFERRED_SIZE, 
                                GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.TRAILING)
                    .addComponent(jPanel1, GroupLayout.DEFAULT_SIZE,
                                  GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 442, Short.MAX_VALUE))
                .addContainerGap())
        );
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
                Node child = getTB(childid);
                node.addChild(childid, child);
                DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(child);
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode,treenode.getChildCount());
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
    public Node getTB(String id){
        try{HashMap hash= (HashMap)client.execute("getResource", new Object[]{id});
            System.out.println(hash.toString());
            String path = hash.get("path").toString();
            String name = path.split("/")[path.split("/").length-1];
            Node node = new Node(id,path,name);
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
                                        ":"+Repository.getResourceAllocatorPort()));
            client = new XmlRpcClient();
            client.setConfig(configuration);
            System.out.println("XMLRPC Client for testbed initialized: "+client);}
        catch(Exception e){System.out.println("Could not conect to "+
                            Repository.host+" :"+Repository.getResourceAllocatorPort()+
                            "for RPC client initialization");}
    }
}