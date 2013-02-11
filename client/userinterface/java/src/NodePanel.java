import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JButton;
import javax.swing.JScrollPane;
import javax.swing.BorderFactory;
import javax.swing.border.BevelBorder;
import java.awt.Color;
import java.awt.Dimension;
import javax.swing.GroupLayout;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JTree;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;
import com.twister.CustomDialog;
import javax.swing.JOptionPane;
import org.apache.xmlrpc.client.XmlRpcClient;

public class NodePanel extends JPanel{
    private Node parent;
    private JTextField tname,tid,tpath;
    private JButton add;
    private DefaultMutableTreeNode treenode;
    private JTree tree;
    private JPanel proppanel;
    private XmlRpcClient client;

    public NodePanel(JTree tree,XmlRpcClient client){
        this.tree = tree;
        this.client = client;
        init();
    }
    
    public void setParent(Node parent,DefaultMutableTreeNode treenode){
        this.parent = parent;
        this.treenode = treenode;
        if(parent!=null&&treenode!=null){
            initNewParent();
            if(!add.isEnabled()){
                add.setEnabled(true);
            }
        } else{
            initNewParent();
            add.setEnabled(false);
        }
        updateProperties();
    }
    
    public Node getNodeParent(){
        return parent;
    }
    
    private void initNewParent(){
        if(parent!=null){
            tname.setText(parent.getName());
            tid.setText(parent.getID());
            tpath.setText(parent.getPath());
        } else {
            tname.setText("");
            tid.setText("");
            tpath.setText("");
        }
    }

    private void init(){
        JLabel name = new JLabel("Name: ");
        JLabel id = new JLabel("ID: ");
        JLabel path = new JLabel("Path:");
        tname = new JTextField();
        tid = new JTextField();
        tid.setEditable(false);
        tpath = new JTextField();
        tpath.setEditable(false);
        JPanel jPanel1 = new JPanel();
        JScrollPane jScrollPane2 = new JScrollPane();
        proppanel = new JPanel();
//         JLabel jLabel1 = new javax.swing.JLabel();
//         JTextField jTextField1 = new javax.swing.JTextField();
//         JLabel jLabel2 = new javax.swing.JLabel();
//         JTextField jTextField2 = new javax.swing.JTextField();

        add = new JButton("Add");
        add.setEnabled(false);


        setBorder(BorderFactory.createBevelBorder(BevelBorder.RAISED));
        jPanel1.setBorder(BorderFactory.createTitledBorder( "Properties"));

        jScrollPane2.setBorder(null);
        jScrollPane2.setPreferredSize(new Dimension(350, 150));

        proppanel.setPreferredSize(new Dimension(280, 150));
        proppanel.setLayout(null);

//         jLabel1.setText("Name:");
//         proppanel.add(jLabel1);
//         jLabel1.setBounds(10, 14, 40, 14);
//         proppanel.add(jTextField1);
//         jTextField1.setBounds(50, 11, 95, 20);
// 
//         jLabel2.setText("Value:");
//         proppanel.add(jLabel2);
//         jLabel2.setBounds(155, 14, 35, 14);
//         proppanel.add(jTextField2);
//         jTextField2.setBounds(195, 11, 100, 20);

        proppanel.add(add);
        add.setBounds(270, 5, 60, 23);

        jScrollPane2.setViewportView(proppanel);

        GroupLayout jPanel1Layout = new GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane2, GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane2, GroupLayout.Alignment.TRAILING, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );
    
    
    GroupLayout optpanLayout = new GroupLayout(this);
        this.setLayout(optpanLayout);
        optpanLayout.setHorizontalGroup(
            optpanLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(optpanLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(optpanLayout.createSequentialGroup()
                        .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(name)
                            .addComponent(id)
                            .addComponent(path))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.TRAILING, false)
                            .addComponent(tid, GroupLayout.Alignment.LEADING, GroupLayout.DEFAULT_SIZE, 151, Short.MAX_VALUE)
                            .addComponent(tname, GroupLayout.Alignment.LEADING)
                            .addComponent(tpath))
                        .addGap(0, 105, Short.MAX_VALUE))
                    .addComponent(jPanel1, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );
        optpanLayout.setVerticalGroup(
            optpanLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(optpanLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(name)
                    .addComponent(tname, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(id)
                    .addComponent(tid, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(path)
                    .addComponent(tpath, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addComponent(jPanel1, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
        
        tname.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                parent.setName(tname.getText());
                ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
            }
        });
        tname.setEditable(false);
        
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String resp = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    NodePanel.this, "Property name", "Name: ");
                if(resp!=null&&!resp.equals("")){
                    try{
                        String path = parent.getParent().getID();
                        String name = parent.getName();
                        String query = "{'"+resp+"':''}";
                        query = client.execute("setResource", new Object[]{name,path,query}).toString();
                        System.out.println(query);
                        if(query.equals("true")){
                            parent.addProperty(resp, "");
                            updateProperties();
                        }
                    }
                    catch(Exception e){e.printStackTrace();}
                }
            }
        });
    }
    
    
    public void updateProperties(){
        proppanel.removeAll();
        if(parent!=null){
            
            
            int size = parent.getProperties().size();
        
            Object [] keys = parent.getProperties().keySet().toArray();
            Object [] values = parent.getProperties().values().toArray();
            
            for(int i=0;i<size;i++){
                
                final JLabel jLabel1 = new JLabel("Name: "+keys[i].toString());
                //final JTextField jTextField1 = new JTextField();
                JLabel jLabel2 = new JLabel("Value:");
                final JTextField jTextField2 = new JTextField();
                
    
                proppanel.add(jLabel1);
                jLabel1.setBounds(5, i*30+5, 150, 14);
    //             proppanel.add(jTextField1);
    //             jTextField1.setBounds(50, i*30+5, 95, 20);
    //             jTextField1.setText(keys[i].toString());
        
    
                proppanel.add(jLabel2);
                jLabel2.setBounds(105, i*30+5, 35, 14);
                proppanel.add(jTextField2);
                jTextField2.setBounds(145, i*30+2, 100, 20);
                jTextField2.setText(values[i].toString());
                jTextField2.addKeyListener(new KeyAdapter(){
                    public void keyReleased(KeyEvent ev){
                        String key = jLabel1.getText().split(": ")[1];
                        String value = jTextField2.getText();
                        parent.addProperty(key,value);
                        String path = parent.getParent().getID();
                        String name = parent.getName();
                        String query = "{'"+key+"':'"+value+"'}";
                        System.out.println(name+" - "+path+" - "+query);
                        try{String resp = client.execute("setResource", new Object[]{name,path,query}).toString();
                            System.out.println(resp);}
                        catch(Exception e){e.printStackTrace();}
                    }
                });
                
                JButton remove = new JButton("Remove");
                remove.setBounds(250, i*30+2, 80, 20);
                remove.addActionListener(new ActionListener(){
                    public void actionPerformed(ActionEvent ev){
                        
                        try{
                            String s = client.execute("deleteResource", new Object[]{parent.getID()+":"+jLabel1.getText().split(": ")[1]}).toString();
                            System.out.println("removing "+parent.getID()+" prop "+s);
                            if(s.equals("true")){
                                parent.getProperties().remove(jLabel1.getText().split(": ")[1]);
                                updateProperties();
                            }
                        } catch(Exception e){
                            e.printStackTrace();
                        }
    
    
                        
                        
                    }
                });
                
                proppanel.add(jLabel1);
                proppanel.add(jLabel2);
                proppanel.add(jTextField2);
                proppanel.add(remove);
            }
            
            add.setBounds(270, (size*30)+2, 60, 23);
            proppanel.add(add);
            proppanel.setPreferredSize(new Dimension(280, (size*30)+30));
        }
        proppanel.repaint();
    }

}
