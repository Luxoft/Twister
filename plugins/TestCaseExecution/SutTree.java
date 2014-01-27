/*
File: SutTree.java ; This file is part of Twister.
Version: 2.002

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
import javax.swing.JTree;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JScrollPane;
import javax.swing.JButton;
import java.awt.BorderLayout;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.awt.Container;
import java.awt.Dimension;
import javax.swing.JTextField;
import javax.swing.AbstractAction;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;
import com.twister.MySftpBrowser;
import java.net.URL;
import javax.swing.DefaultComboBoxModel;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import javax.swing.tree.TreeSelectionModel;
import javax.swing.tree.TreePath;
import java.util.Enumeration;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;

public class SutTree extends JPanel{
    public JTree filestree;
    private DefaultMutableTreeNode filesroot,userroot,globalroot;
    private JButton newfile,openfile,deletefile,
                    refreshlist,importxml,exportxml,renamefile;
    private XmlRpcClient client;
    
    public SutTree(){
        initializeRPC();
        filestree = new JTree();
        filestree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        filesroot = new DefaultMutableTreeNode("root", true);
        userroot = new DefaultMutableTreeNode("User", true);
        globalroot = new DefaultMutableTreeNode("Global", true);
        filesroot.add(userroot);
        filesroot.add(globalroot);
        DefaultTreeModel treemodel = new DefaultTreeModel(filesroot,true);
        filestree.setModel(treemodel);
        filestree.expandRow(1);
        filestree.setRootVisible(false);
        filestree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                TreePath tp = filestree.getPathForLocation(ev.getX(), ev.getY());
                if(tp!=null){
                    newfile.setEnabled(true);
                    final DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();                    
                    if(PermissionValidator.canChangeSutLock() && tp!=null && (ev.getButton() == MouseEvent.BUTTON3) && (treenode.getUserObject() instanceof SUT )){
                        final SUT sut = (SUT)treenode.getUserObject();
                        filestree.setSelectionPath(tp);
                        JPopupMenu p = new JPopupMenu();
                        JMenuItem item = new JMenuItem("Lock");
                        item.addActionListener(new ActionListener(){
                            public void actionPerformed(ActionEvent ev){
                                try{String resp = client.execute("lockSut", new Object[]{"/"+sut.getName()+sut.getRoot()}).toString();
                                if(resp.equals("2")){
                                    sut.setLock(RunnerRepository.user);
                                    ((DefaultTreeModel)filestree.getModel()).nodeChanged(treenode);
                                    openfile.setEnabled(false);
                                    renamefile.setEnabled(false);
                                    deletefile.setEnabled(false);
                                } else {
                                    System.out.println(sut.getName()+" was not locked, CE respons: "+resp);
                                }
                            } catch(Exception e){e.printStackTrace();}
                            }});
                        p.add(item);
                        if(!sut.getLock().equals("")||!sut.getReserved().equals(""))item.setEnabled(false);
                        item = new JMenuItem("Unlock");
                        item.addActionListener(new ActionListener(){
                            public void actionPerformed(ActionEvent ev){
                                try{String resp = client.execute("unlockSut", new Object[]{"/"+sut.getName()+sut.getRoot()}).toString();
                                    if(resp.equals("1")){
                                        sut.setLock("");
                                        ((DefaultTreeModel)filestree.getModel()).nodeChanged(treenode);
                                        openfile.setEnabled(true);
                                        renamefile.setEnabled(true);
                                        deletefile.setEnabled(true);
                                    } else {
                                        System.out.println(sut.getName()+" was not unlocked, CE respons: "+resp);  
                                    }
                                } catch (Exception e){
                                    e.printStackTrace();
                                }
                            }});
                        p.add(item);
                        if(!sut.getLock().equals(RunnerRepository.user))item.setEnabled(false);
                        p.show(filestree,ev.getX(),ev.getY());
                    } else {
                        treeContextOptions(tp);
                    }
                } else {
                    newfile.setEnabled(false);
                    treeContextOptions(tp);
                }
                
            }});
        setLayout(new BorderLayout());
        JScrollPane sp2 = new JScrollPane(filestree);
        add(sp2,BorderLayout.CENTER);
        JPanel filesoption = new JPanel();
        add(filesoption,BorderLayout.SOUTH);
        if(PermissionValidator.canChangeSut()){
            newfile = new JButton("New");
            setNewAction();
            openfile = new JButton("Open");
            setOpenAction();
            renamefile = new JButton("Rename");
            setRenameAction();
            deletefile = new JButton("Delete");
            setDeleteAction();
            refreshlist = new JButton("Refresh List");
            setRefreshAction();
            importxml = new JButton("Import XML");
            setImportAction();
            exportxml = new JButton("Export XML");
            setExportAction();
            filesoption.add(newfile);
            filesoption.add(openfile);
            filesoption.add(renamefile);
            filesoption.add(deletefile);
            filesoption.add(refreshlist);
            filesoption.add(importxml);
            filesoption.add(exportxml);
            openfile.setEnabled(false);
            renamefile.setEnabled(false);
            deletefile.setEnabled(false);
            exportxml.setEnabled(false);
            newfile.setEnabled(false);
        }
        getSUT();
    }
    
    public void treeContextOptions(TreePath tp){
        if (tp != null){
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
            if(treenode.getUserObject() instanceof SUT){//sut selected
                exportxml.setEnabled(true);
                SUT sut = (SUT)treenode.getUserObject();
                String reserved = sut.getReserved();
                if(reserved.equals("")&&sut.getLock().equals("")){// sut was not reserved and not locked
                    openfile.setEnabled(true);
                    renamefile.setEnabled(true);
                    deletefile.setEnabled(true);
                } else {//sut was reserved or locked
                    renamefile.setEnabled(false);
                    openfile.setEnabled(false);
                    deletefile.setEnabled(false);
                }
            } else {//root selected
                openfile.setEnabled(false);
                renamefile.setEnabled(false);
                deletefile.setEnabled(false);
            }
        } else {//nothing selected
            filestree.setSelectionPath(null);
            openfile.setEnabled(false);
            renamefile.setEnabled(false);
            deletefile.setEnabled(false);
            exportxml.setEnabled(false);
        }
    
    }
    
    public void releaseAllSuts(){
        Enumeration en = userroot.children();
        SUT sut;
        while(en.hasMoreElements()){
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)en.nextElement();
            sut = (SUT)(treenode).getUserObject();
            if(sut.getReserved().equals(RunnerRepository.user)){
                System.out.println("Releasing sut: "+sut.getName());
                try{client.execute("discardAndReleaseReservedSut", new Object[]{"/"+sut.getName()+".user"}).toString();}
                catch(Exception e){
                    System.out.println("Could not release sut: "+sut.getName());
                    e.printStackTrace();}
            }
        }
        en = globalroot.children();
        while(en.hasMoreElements()){
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)en.nextElement();
            sut = (SUT)(treenode).getUserObject();
            if(sut.getReserved().equals(RunnerRepository.user)){
                System.out.println("Releasing sut: "+sut.getName());
                try{client.execute("discardAndReleaseReservedSut", new Object[]{"/"+sut.getName()+".system"}).toString();}
                catch(Exception e){
                    System.out.println("Could not release sut: "+sut.getName());
                    e.printStackTrace();}
            }
        }
    }
    
    private void setNewAction(){
        newfile.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                JPanel p = new JPanel();
                p.setLayout(null);
                p.setPreferredSize(new Dimension(250,200));
                JLabel sut = new JLabel("SUT name: ");
                sut.setBounds(5,5,80,25);
                JTextField tsut = new JTextField();
                tsut.setBounds(90,5,155,25);
                JLabel ep = new JLabel("Run on EP's: ");
                ep.setBounds(5,35,80,25);
                JList tep = new JList();
                JScrollPane scep = new JScrollPane(tep);
                scep.setBounds(90,35,155,150);
                p.add(sut);
                p.add(tsut);
                p.add(ep);
                p.add(scep);
                populateEPs(tep,null);
                
                
                TreePath tp = filestree.getSelectionPath();
                DefaultMutableTreeNode selected = (DefaultMutableTreeNode)tp.getLastPathComponent();
                DefaultMutableTreeNode root = (DefaultMutableTreeNode)tp.getPathComponent(1);
                String add = "";
                if(root.toString().equals("User")){
                    add = ".user";
                } else {
                    add = ".system";
                }
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                            JOptionPane.OK_CANCEL_OPTION, SutTree.this, "New SUT",null);
                            
                if(resp == JOptionPane.OK_OPTION&&!tsut.getText().equals("")){
                    if(add.equals(".user")&&RunnerRepository.window.mainpanel.p4.getSut().sut.checkExistingName(userroot, tsut.getText(), null)){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,SutTree.this,"Warning", 
                                        "This name is already used, please use different name.");
                         return;
                    } else if(add.equals(".system")&&RunnerRepository.window.mainpanel.p4.getSut().sut.checkExistingName(globalroot, tsut.getText(), null)){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,SutTree.this,"Warning", 
                                        "This name is already used, please use different name.");
                         return;
                    }
//                     if(checkExistingName(root, tsut.getText(),null)){
//                         CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,SUTEditor.this,"Warning", 
//                                         "This name is already used, please use different name.");
//                          return;
//                     }
                    try{
                        StringBuilder sb = new StringBuilder();
                        for(int i=0;i<tep.getSelectedValuesList().size();i++){
                            sb.append(tep.getSelectedValuesList().get(i).toString());
                            sb.append(";");
                        }
                        String query = "{'_epnames_"+RunnerRepository.user+"':'"+sb.toString()+"'}";
                        String user = tsut.getText();
                        String respons = client.execute("setSut", new Object[]{user+add,"/",query}).toString();
                        if(respons.indexOf("ERROR")==-1){
                            DefaultTreeModel model = (DefaultTreeModel)filestree.getModel();
                            SUT s = new SUT(user,add);
                            DefaultMutableTreeNode element = new DefaultMutableTreeNode(s,false);
                            if(add.equals(".system")){
                                model.insertNodeInto(element, globalroot, globalroot.getChildCount());
                            } else if(add.equals(".user")){
                                model.insertNodeInto(element, userroot, userroot.getChildCount());
                            }
                            RunnerRepository.window.mainpanel.p1.suitaDetails.setComboTBs();
                        } else {
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,SutTree.this,"Warning", respons);
                        }
                    }
                    catch(Exception e){
                        e.printStackTrace();
                    }   
                }
            }
        });
    }
    
    public void addUserNode(DefaultMutableTreeNode element){
        DefaultTreeModel model = (DefaultTreeModel)filestree.getModel();
        model.insertNodeInto(element, userroot, userroot.getChildCount());
    }
    
    private void setOpenAction(){
        openfile.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                TreePath tp = filestree.getSelectionPath();
                SUT sut = (SUT)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject();
                if(sut.getReserved().equals(RunnerRepository.user)){//if already reserved by user
                    RunnerRepository.window.mainpanel.p4.getSut().sut.getSUT(sut.getName()+sut.getRoot(),(DefaultMutableTreeNode)tp.getLastPathComponent(),true);
                    return;
                } else if(sut.getReserved().equals("")){ //if it was not reserved at all
                    if(reserveSut(sut)){
                        RunnerRepository.window.mainpanel.p4.getSut().sut.closeSut();
                        sut.setReserved(RunnerRepository.user);
                        RunnerRepository.window.mainpanel.p4.getSut().sut.getSUT(sut.getName()+sut.getRoot(),(DefaultMutableTreeNode)tp.getLastPathComponent(),true);
                        filestree.setSelectionPath(null);
                        openfile.setEnabled(false);
                        renamefile.setEnabled(false);   
                        deletefile.setEnabled(false);
                        exportxml.setEnabled(false);
                        ((DefaultTreeModel)filestree.getModel()).nodeChanged((DefaultMutableTreeNode)tp.getLastPathComponent());
                    }
//                     try{
//                         String resp = client.execute("reserveSut", new Object[]{"/"+sut.getName()+sut.getRoot()}).toString();
//                         if(resp.equals("3")){
//                             RunnerRepository.window.mainpanel.p4.getSut().sut.getSUT(sut.getName()+sut.getRoot());
//                         } else {
//                             System.out.println(resp);
//                             CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"Error", "Could not reserve sut");
//                         }
//                     }
//                     catch(Exception e){
//                         e.printStackTrace();
//                     }
                } else { //it was reserved by other user
                    RunnerRepository.window.mainpanel.p4.getSut().sut.closeSut();
                    //sut.setReserved(RunnerRepository.user);
                    RunnerRepository.window.mainpanel.p4.getSut().sut.getSUT(sut.getName()+sut.getRoot(),(DefaultMutableTreeNode)tp.getLastPathComponent(),false);
                    filestree.setSelectionPath(null);
                    openfile.setEnabled(false);
                    renamefile.setEnabled(false);   
                    deletefile.setEnabled(false);
                    exportxml.setEnabled(false);
                    ((DefaultTreeModel)filestree.getModel()).nodeChanged((DefaultMutableTreeNode)tp.getLastPathComponent());
                }
            }
        });
    }
    
    public boolean reserveSut(SUT sut){
        try{String resp = client.execute("reserveSut", new Object[]{"/"+sut.getName()+sut.getRoot()}).toString();
            if(resp.equals("3")){
                return true;
            } else {
                System.out.println(resp);
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"Error", "Could not reserve sut");
                return false;
            }
        } catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    private void setRenameAction(){
        renamefile.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                TreePath tp = filestree.getSelectionPath();
                if(tp.getPathCount()==0)return;
                DefaultMutableTreeNode selected = (DefaultMutableTreeNode)tp.getLastPathComponent();
                DefaultMutableTreeNode root = (DefaultMutableTreeNode)tp.getPathComponent(1);
                String reserved = ((SUT)selected.getUserObject()).getReserved();
                String name= ((SUT)selected.getUserObject()).getName();
                if(!reserved.equals(RunnerRepository.user)&&!reserved.equals(""))return;
                String add = "";
                if(root.toString().equals("User")){
                    add = ".user";
                } else {
                    add = ".system";
                }
//                 if(root.toString().equals("User")){
                    if(reserved.equals("")){
                        if(!reserveSut(((SUT)selected.getUserObject()))){
                            return;
                        }
                    }
//                     String torename = "/"+name+".user";
                    String torename = "/"+name+add;
                    try{
                        String filename = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
                                             JOptionPane.OK_CANCEL_OPTION
                                             ,SutTree.this,
                                             "Sut Name", "Please enter sut name");
                        if(filename!=null&&!filename.equals("NULL")){
                            if(add.equals(".user")&&RunnerRepository.window.mainpanel.p4.getSut().sut.checkExistingName(userroot, filename, null)){
                                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,SutTree.this,"Warning", 
                                                "This name is already used, please use different name.");
                                 return;
                            } else if(add.equals(".system")&&RunnerRepository.window.mainpanel.p4.getSut().sut.checkExistingName(globalroot, filename, null)){
                                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,SutTree.this,"Warning", 
                                                "This name is already used, please use different name.");
                                 return;
                            }
                            String query = client.execute("renameSut", new Object[]{torename,filename+add}).toString();
                            if(query.equals("true")){
                                ((SUT)selected.getUserObject()).setName(filename);
                                ((DefaultTreeModel)filestree.getModel()).nodeChanged(selected);
                                if(reserved.equals("")){//sut was not initialy reserved
                                    String resp = client.execute("saveAndReleaseReservedSut", new Object[]{torename}).toString();
                                } else {//sut was allready reserved and opened
                                    RunnerRepository.window.mainpanel.p4.getSut().sut.setRootSutName(filename+add);
                                }
                                RunnerRepository.window.mainpanel.p1.suitaDetails.setComboTBs();
                            } else {
                                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,SutTree.this,"Warning", query);
                            }
                        }
                        
                        
                    } catch(Exception e){
                        System.out.println("Could not rename sut: "+torename);
                        e.printStackTrace();
                    }
//                 }
            }});}
    
    private void setDeleteAction(){
        deletefile.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                TreePath tp = filestree.getSelectionPath();
                if(tp.getPathCount()==0)return;
                DefaultMutableTreeNode selected = (DefaultMutableTreeNode)tp.getLastPathComponent();
                DefaultMutableTreeNode root = (DefaultMutableTreeNode)tp.getPathComponent(1);
                String torem = "";
                if(root.toString().equals("User")){
                    torem = "/"+selected.toString()+".user";                    
                } else {
                    torem = "/"+selected.toString()+".system";
                }
                try{String s = client.execute("deleteSut", new Object[]{torem}).toString();
                    if(s.indexOf("ERROR")==-1){
                        ((DefaultTreeModel)filestree.getModel()).removeNodeFromParent(selected);
                        RunnerRepository.window.mainpanel.p1.suitaDetails.setComboTBs();
                        openfile.setEnabled(false);
                        renamefile.setEnabled(false);   
                        deletefile.setEnabled(false);
                        exportxml.setEnabled(false);
                    } else {
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", "Cannot delete SUT file. "+s);
                    }
                } catch(Exception e){
                    System.out.println("Could not delete sut: "+torem);
                    e.printStackTrace();
                }
            }
        });
    }
    
    private void setRefreshAction(){
        refreshlist.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                getSUT();
            }
        });
    }
    
    private void setImportAction(){
        importxml.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Container c;
                if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                else c = RunnerRepository.window;
                final JTextField tf = new JTextField();
                new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,c,false).setAction(new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            String resp = client.execute("import_xml", new Object[]{tf.getText(),2}).toString();
                            System.out.println("resp: "+resp);
                            if(resp.equals("true")){
                                getSUT();
                                RunnerRepository.window.mainpanel.p1.suitaDetails.setComboTBs();
                            } else {
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", "Could not import!");
                            }
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                });
                
                
                
            }
        });
    }
    
    private void setExportAction(){
        exportxml.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Container c;
                if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                else c = RunnerRepository.window;
                final JTextField tf = new JTextField();
                try{
                    tf.setText(RunnerRepository.getTestConfigPath());
                }catch(Exception e){
                    e.printStackTrace();
                }
                AbstractAction action = new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            SUT sut = (SUT)((DefaultMutableTreeNode)filestree.getSelectionPath().getLastPathComponent()).getUserObject();
                            String sutname = sut.getName();
                            System.out.println("export_sut_xml: "+tf.getText()+"/"+sutname+".user");
                            String resp = client.execute("export_sut_xml", new Object[]{tf.getText(),"/"+sutname+".user"}).toString();
                            if(resp.equals("false")){
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", "Could not save");
                            }
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                };
                MySftpBrowser browser = new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,c,false);
                browser.setAction(action);
                browser.setButtonText("Save");
            }
        });
    }
    
    /*
     * get ep's list from
     * CE and populate the list
     */
    public void populateEPs(JList tep, String eps){
        try{
            String query = RunnerRepository.getRPCClient().execute("listEPs", new Object[]{RunnerRepository.user}).toString();
            String [] vecresult = query.split(",");
            tep.setModel(new DefaultComboBoxModel(vecresult));
            ArrayList<String> array = new ArrayList<String>(Arrays.asList(vecresult));
            if(eps!=null){
                String [] strings = eps.split(";");
                int [] sel = new int[strings.length];
                for(int i=0;i<strings.length;i++){
                    sel[i]=array.indexOf(strings[i]);
                }
                tep.setSelectedIndices(sel);
            }
        } catch (Exception e){e.printStackTrace();}
    }
    
    public String [] getSutsName(){
        try{
            HashMap hash= (HashMap)client.execute("getSut", new Object[]{"/"});
            Object[] children = (Object[])hash.get("children");
            String name,path;
            StringBuilder b = new StringBuilder();
            for(Object o:children){
                hash= (HashMap)client.execute("getSut", new Object[]{o.toString()});
                path = hash.get("path").toString();
                name = path.split("/")[path.split("/").length-1];
                name = name.replace(".user", "");
                name = name.replace(".system", "");
                b.append(name);
                b.append(";");
            }
            return b.toString().split(";");
        } catch(Exception e){
            System.out.println("There was an error in getting sut names from server");
            e.printStackTrace();
            return null;
        }
    }
    
    public void getSUT(){
        try{HashMap hash= (HashMap)client.execute("getSut", new Object[]{"/"});
            Object[] children = (Object[])hash.get("children");
            DefaultMutableTreeNode child;
            userroot.removeAllChildren();
            globalroot.removeAllChildren();
            DefaultTreeModel model = (DefaultTreeModel)filestree.getModel();
            String name,path,eps;
            Object[] subchildren;
            for(Object o:children){
                String root = ".system";
                boolean user = false;
                hash= (HashMap)client.execute("getSut", new Object[]{o.toString()});
                path = hash.get("path").toString();
                name = path.split("/")[path.split("/").length-1];
                if(name.indexOf(".user")!=-1){
                    user = true;
                    root = ".user";
                }
                name = name.replace(".user", "");
                name = name.replace(".system", "");                
                SUT s = new SUT(name,root);
                String lock = client.execute("isSutLocked", new Object[]{"/"+name+root}).toString();
                if(lock.equals("false"))s.setLock("");
                else s.setLock(lock);
                child = new DefaultMutableTreeNode(s,false);
                if(user){
                    model.insertNodeInto(child, userroot, userroot.getChildCount());
                } else {
                    model.insertNodeInto(child, globalroot, globalroot.getChildCount());
                }
                Enumeration en = userroot.children();
                SUT node;
                while(en.hasMoreElements()){
                    DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)en.nextElement();
                    node = (SUT)treenode.getUserObject();
                    node.setReserved(getSUTReservdUser(node.getName()+".user"));
                    ((DefaultTreeModel)filestree.getModel()).nodeChanged(treenode);
                }
                en = globalroot.children();
                while(en.hasMoreElements()){
                    DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)en.nextElement();
                    node = (SUT)treenode.getUserObject();
                    node.setReserved(getSUTReservdUser(node.getName()+".system"));
                    ((DefaultTreeModel)filestree.getModel()).nodeChanged(treenode);
                }
                model.reload();
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    
    /*
     * get from server user that reserved sut
     */
    public String getSUTReservdUser(String name){
        try{String resp = client.execute("isSutReserved", new Object[]{"/"+name}).toString();
            if(resp.equals("false"))return "";
            else return resp;
        }
        catch(Exception e){e.printStackTrace();
            return "";
        }
    }
    
    
    /*
     * initialize RPC connection
     * based on host an port of 
     * resource allocator specified in config
     */
    public void initializeRPC(){
        try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
            configuration.setServerURL(new URL("http://"+RunnerRepository.host+
                                        ":"+RunnerRepository.getCentralEnginePort()+"/ra/"));
            configuration.setEnabledForExtensions(true);
            configuration.setBasicPassword(RunnerRepository.password);
            configuration.setBasicUserName(RunnerRepository.user);
            client = new XmlRpcClient();
            client.setConfig(configuration);
            System.out.println("XMLRPC Client for SutTree initialized: "+client);}
        catch(Exception e){System.out.println("Could not conect to "+
                            RunnerRepository.host+" :"+RunnerRepository.getCentralEnginePort()+"/ra/"+
                            "for RPC client initialization");}
    }
    
}
