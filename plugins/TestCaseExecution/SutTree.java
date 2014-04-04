/*
File: SutTree.java ; This file is part of Twister.
Version: 2.014

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
import javax.swing.DefaultListModel;
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
    public DefaultMutableTreeNode filesroot,userroot,globalroot;
    private JButton newfile,openfile,deletefile,
                    refreshlist,importxml,exportxml,renamefile;
    private XmlRpcClient client;
    public JScrollPane sp2;
    
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
                    importxml.setEnabled(true);
                    newfile.setEnabled(true);
                    final DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();                    
                    if(PermissionValidator.canChangeSutLock() && tp!=null && (ev.getButton() == MouseEvent.BUTTON3) && (treenode.getUserObject() instanceof SUT )){
                        final SUT sut = (SUT)treenode.getUserObject();
                        filestree.setSelectionPath(tp);
                        JPopupMenu p = new JPopupMenu();
                        JMenuItem item = new JMenuItem("Lock");
                        item.addActionListener(new ActionListener(){
                            public void actionPerformed(ActionEvent ev){
                                try{String resp = client.execute("lockSut", new Object[]{"/"+sut.getName()+sut.getRoot(),"",RunnerRepository.user}).toString();
                                if(resp.indexOf("*ERROR*")==-1){
                                    sut.setLock(RunnerRepository.user);
                                    ((DefaultTreeModel)filestree.getModel()).nodeChanged(treenode);
                                    openfile.setEnabled(false);
                                    renamefile.setEnabled(false);
                                    deletefile.setEnabled(false);
                                } else {
                                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", resp);
                                    System.out.println(sut.getName()+" was not locked, CE respons: "+resp);
                                }
                            } catch(Exception e){e.printStackTrace();}
                            }});
                        p.add(item);
                        if(!sut.getLock().equals("")||!sut.getReserved().equals(""))item.setEnabled(false);
                        item = new JMenuItem("Unlock");
                        item.addActionListener(new ActionListener(){
                            public void actionPerformed(ActionEvent ev){
                                try{String resp = client.execute("unlockSut", new Object[]{"/"+sut.getName()+sut.getRoot(),"",RunnerRepository.user}).toString();
                                    if(resp.indexOf("*ERROR*")==-1){
                                        sut.setLock("");
                                        ((DefaultTreeModel)filestree.getModel()).nodeChanged(treenode);
                                        openfile.setEnabled(true);
                                        renamefile.setEnabled(true);
                                        deletefile.setEnabled(true);
                                    } else {
                                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", resp);
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
                    importxml.setEnabled(false);
                    newfile.setEnabled(false);
                    treeContextOptions(tp);
                }
                
            }});
        setLayout(new BorderLayout());
        sp2 = new JScrollPane(filestree);
        add(sp2,BorderLayout.CENTER);
        JPanel filesoption = new JPanel();
        add(filesoption,BorderLayout.SOUTH);
        newfile = new JButton("New");
        openfile = new JButton("Open");
        renamefile = new JButton("Rename");
        deletefile = new JButton("Delete");
        refreshlist = new JButton("Refresh List");
        importxml = new JButton("Import XML");
        exportxml = new JButton("Export XML");
        if(PermissionValidator.canChangeSut()){
            setNewAction();
            setOpenAction();
            setRenameAction();
            setDeleteAction();
            setRefreshAction();
            setImportAction();
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
            importxml.setEnabled(false);
        }
        getSUT();
    }
    
    public void treeContextOptions(TreePath tp){
        if (tp != null){
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
            if(treenode.getUserObject() instanceof SUT){//sut selected
                openfile.setEnabled(true);
                SUT sut = (SUT)treenode.getUserObject();
                String reserved = sut.getReserved();
                if(reserved.equals("")&&sut.getLock().equals("")){// sut was not reserved and not locked
                    exportxml.setEnabled(true);
                    renamefile.setEnabled(true);
                    deletefile.setEnabled(true);
                } else {//sut was reserved or locked
                    renamefile.setEnabled(false);
                    //openfile.setEnabled(false);
                    deletefile.setEnabled(false);
                    exportxml.setEnabled(false);
                }
            } else {//root selected
                openfile.setEnabled(false);
                renamefile.setEnabled(false);
                deletefile.setEnabled(false);
                exportxml.setEnabled(false);
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
                try{System.out.println("discarding: "+"/"+sut.getName()+".user");
                    String resp = client.execute("discardAndReleaseReservedSut", new Object[]{"/"+sut.getName()+".user",RunnerRepository.user}).toString();
                    System.out.println("CE response: "+resp);
                    sut.setReserved("");
//                     if(resp.indexOf("*ERROR*")!=-1){
//                         CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", resp);
//                     }
                }
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
                try{System.out.println("discarding: "+"/"+sut.getName()+".system");
                    String resp = client.execute("discardAndReleaseReservedSut", new Object[]{"/"+sut.getName()+".system",RunnerRepository.user}).toString();
                    System.out.println("CE response: "+resp);                    
                    sut.setReserved("");
//                     if(resp.indexOf("*ERROR*")!=-1){
//                         CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", resp);
//                     }
                }
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
                    try{
                        StringBuilder sb = new StringBuilder();
                        for(int i=0;i<tep.getSelectedValuesList().size();i++){
                            sb.append(tep.getSelectedValuesList().get(i).toString());
                            sb.append(";");
                        }
                        String query = "{'_epnames_"+RunnerRepository.user+"':'"+sb.toString()+"'}";
                        String user = tsut.getText();
                        String respons = client.execute("setSut", new Object[]{user+add,"/",query,RunnerRepository.user}).toString();
                        if(respons.indexOf("*ERROR*")==-1){
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
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", respons);
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
                } else if(sut.getReserved().equals("")&&sut.getLock().equals("")){ //if it was not reserved at all
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
                } else { //it was reserved by other user
                    RunnerRepository.window.mainpanel.p4.getSut().sut.closeSut();
                    RunnerRepository.window.mainpanel.p4.getSut().sut.getSUT(sut.getName()+sut.getRoot(),(DefaultMutableTreeNode)tp.getLastPathComponent(),false);
                    filestree.setSelectionPath(null);
                    renamefile.setEnabled(false);   
                    deletefile.setEnabled(false);
                    exportxml.setEnabled(false);
                    ((DefaultTreeModel)filestree.getModel()).nodeChanged((DefaultMutableTreeNode)tp.getLastPathComponent());
                }
            }
        });
    }
    
    public boolean reserveSut(SUT sut){
        try{String resp = client.execute("reserveSut", new Object[]{"/"+sut.getName()+sut.getRoot(),RunnerRepository.user}).toString();
            if(resp.indexOf("*ERROR*")==-1){
                return true;
            } else {
                System.out.println(resp);
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"Error", "Could not reserve sut, CE error: "+resp);
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
                String torename = name+add;
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
                        String query = client.execute("renameSut", new Object[]{torename,filename+add,RunnerRepository.user}).toString();
                        if(query.indexOf("*ERROR*")==-1){
                            ((SUT)selected.getUserObject()).setName(filename);
                            ((DefaultTreeModel)filestree.getModel()).nodeChanged(selected);
                            if(reserved.equals("")){//sut was not initialy reserved
                            } else {//sut was allready reserved and opened
                                RunnerRepository.window.mainpanel.p4.getSut().sut.setRootSutName(filename+add);
                            }
                            RunnerRepository.window.mainpanel.p1.suitaDetails.setComboTBs();
                        } else {
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", query);
                        }
                    }
                } catch(Exception e){
                    System.out.println("Could not rename sut: "+torename);
                    e.printStackTrace();
                }
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
                try{String s = client.execute("deleteSut", new Object[]{torem,RunnerRepository.user}).toString();
                    if(s.indexOf("*ERROR*")==-1){
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
                try{tf.setText(RunnerRepository.getSutPath());}
                catch(Exception e){
                    tf.setText("");
                }
                new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,RunnerRepository.CENTRALENGINEPORT,tf,c,false).setAction(new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{TreePath tp = filestree.getSelectionPath();
                            DefaultMutableTreeNode selected = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            DefaultMutableTreeNode root = (DefaultMutableTreeNode)tp.getPathComponent(1);
                            String type = "";
                            if(root.toString().equals("User")){
                                type = "user";
                            } else {
                                type = "system";
                            }
                            String resp = client.execute("import_sut_xml", new Object[]{tf.getText(),type,RunnerRepository.user}).toString();
                            if(resp.indexOf("*ERROR*")==-1){
                                getSUT();
                                RunnerRepository.window.mainpanel.p1.suitaDetails.setComboTBs();
                            } else {
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", "Could not import! CE error: "+resp);
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
                    tf.setText(RunnerRepository.getSutPath());
                }catch(Exception e){
                    e.printStackTrace();
                }
                AbstractAction action = new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            SUT sut = (SUT)((DefaultMutableTreeNode)filestree.getSelectionPath().getLastPathComponent()).getUserObject();
                            TreePath tp = filestree.getSelectionPath();
                            DefaultMutableTreeNode selected = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            DefaultMutableTreeNode root = (DefaultMutableTreeNode)tp.getPathComponent(1);
                            String add = "";
                            if(root.toString().equals("User")){
                                add = ".user";
                            } else {
                                add = ".system";
                            }
                            String sutname = sut.getName()+add;
                            String resp = client.execute("export_sut_xml", new Object[]{tf.getText(),"/"+sutname,RunnerRepository.user}).toString();
                            if(resp.indexOf("*ERROR*")!=-1){
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", "Could not save, CE error: "+resp);
                            }
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                };
                MySftpBrowser browser = new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,RunnerRepository.CENTRALENGINEPORT,tf,c,false);
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
            DefaultListModel dlm = new DefaultListModel();
            for(String ep:vecresult){
                dlm.addElement(ep);
            }
            tep.setModel(dlm);
            //tep.setModel(new DefaultComboBoxModel(vecresult));
            //tep.setModel(new DefaultListModel(vecresult));
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
            Object ob = client.execute("listAllSuts", new Object[]{RunnerRepository.user});
            if(ob.toString().indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", ob.toString());
            }
            Object [] array = (Object[])ob;
            StringBuilder b = new StringBuilder();
            for(Object object:array){
                HashMap hash = (HashMap)object;
                b.append(hash.get("name").toString());
                b.append(";");
            }
            return b.toString().split(";");
        } catch(Exception e){
            System.out.println("There was an error in getting sut names from server");
            e.printStackTrace();
            return null;
        }
    }

    public String [][] getSutFiles(){
        try{Object ob = client.execute("listAllSuts", new Object[]{RunnerRepository.user});
            if(ob.toString().indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", ob.toString());
            }
            Object [] array = (Object[])ob;
            String name;
            StringBuilder sb = new StringBuilder();
            HashMap hash;
            StringBuilder statuses = new StringBuilder();
            StringBuilder user = new StringBuilder();
            for(Object object:array){
                hash = (HashMap)object;
                name = hash.get("name").toString();
                name = name.replace(".user", "(user)");
                name = name.replace(".system", "(system)");
                sb.append(name);
                sb.append(";");
                String status = hash.get("status").toString();
                statuses.append(status);
                statuses.append(";");
                if(!status.equals("free")){
                    user.append(hash.get("user").toString());
                    user.append(";");
                }else {
                    user.append(" ");
                    user.append(";");
                }
            }
                            
            String [] suts = sb.toString().split(";");
            String [] stats = statuses.toString().split(";");
            String [] users = user.toString().split(";");
            String [][] respons = new String[suts.length][3];
            for(int i=0;i<suts.length;i++){
                respons[i][0] = suts[i];
                respons[i][1] = stats[i];
                respons[i][2] = users[i];
            }
            return respons;
        } catch (Exception e){
            e.printStackTrace();
            return null;
        }
    }
    
    public void getSUT(){
        try{Object ob = client.execute("listAllSuts", new Object[]{RunnerRepository.user});
            if(ob.toString().indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutTree.this,"ERROR", ob.toString());
            }
            userroot.removeAllChildren();
            globalroot.removeAllChildren();
            Object [] array = (Object[])ob;
            DefaultMutableTreeNode child;
            DefaultTreeModel model = (DefaultTreeModel)filestree.getModel();
            String name,path,root;
            Object[] subchildren;
            HashMap hash;
            boolean isuser;
            SUT s;
            for(Object object:array){
                hash = (HashMap)object;
                root = ".system";
                isuser = false;
                name = hash.get("name").toString();
                if(name.indexOf(".user")!=-1){
                    isuser = true;
                    root = ".user";
                }
                name = name.replace(".user", "");
                name = name.replace(".system", "");                
                s = new SUT(name,root);
                String status = hash.get("status").toString();
                if(!status.equals("free")){
                    String user = hash.get("user").toString();
                    if(status.equals("locked")){
                        s.setLock(user);
                    } else if(status.equals("reserved")){
                        s.setReserved(user);
                    }
                }
                child = new DefaultMutableTreeNode(s,false);
                if(isuser){
                    model.insertNodeInto(child, userroot, userroot.getChildCount());
                } else {
                    model.insertNodeInto(child, globalroot, globalroot.getChildCount());
                }
                filestree.expandPath(new TreePath(userroot.getPath()));
                filestree.expandPath(new TreePath(globalroot.getPath()));
            }
            model.reload();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    public void releaseSut(String sut){
        DefaultMutableTreeNode node;
        if(sut.indexOf("user")!=-1){
            node = userroot;
            sut = sut.replace(".user", "");
        } else {
            sut = sut.replace(".system", "");            
            node = globalroot;
        }
        node = findInNode(node,sut);
        if(node!=null){
            ((SUT)node.getUserObject()).setReserved("");
            ((DefaultTreeModel)filestree.getModel()).nodeChanged(node);
        } else {
            System.out.println("Could not find: "+sut);
        }
    }
    
    private DefaultMutableTreeNode findInNode(DefaultMutableTreeNode node, String name){
        if(node==null)return null;
        int nr = node.getChildCount();
        String compare = "";
        for(int i=0;i<nr;i++){
            compare = ((DefaultMutableTreeNode)node.getChildAt(i)).toString().split(" - Reserved by: ")[0];
            if(compare.equalsIgnoreCase(name)){
                return (DefaultMutableTreeNode)node.getChildAt(i);
            }
        }
        return null;
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
