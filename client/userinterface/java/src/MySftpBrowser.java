/*
File: MySftpBrowser.java ; This file is part of Twister.

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
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JTextField;
import javax.swing.JComboBox;
import javax.swing.JList;
import java.awt.Component;
import javax.swing.DefaultListCellRenderer;
import javax.swing.ImageIcon;
import java.awt.Image;
import java.io.InputStream;
import javax.imageio.ImageIO;
import javax.swing.SwingConstants;
import javax.swing.ListSelectionModel;
import javax.swing.border.EmptyBorder;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import com.jcraft.jsch.ChannelSftp;
import javax.swing.GroupLayout;
import javax.swing.SwingConstants;
import javax.swing.LayoutStyle.ComponentPlacement;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import java.util.Properties;
import java.util.Vector;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import com.jcraft.jsch.SftpException;
import java.util.Collections;
import javax.swing.DefaultListModel;
import javax.swing.ListModel;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.Container;

public class MySftpBrowser extends JFrame {    
    private JPanel  main;
    private JList browser;
    private JButton cancel;
    private JLabel filename;
    private JScrollPane jScrollPane2;
    private JLabel look;
    private JButton open;
    private JTextField tfilename;
    private JComboBox tree;
    private ChannelSftp c;
    private DefaultListModel model;
    private JButton up;
    private JTextField text;
    private ItemListener listener;
    private Container container;
    
    /*
     * c - SFTP connection initialized in repository
     * text - the jtextfield that holds the path
     * container - the parent for sftp browser
     */
    public MySftpBrowser(ChannelSftp c, JTextField text, final Container container) {
        this.text = text;
        this.c = c;
        this.container = container;
        initComponents();
        add(main);
        setAlwaysOnTop(true);
        container.setEnabled(false);
        addWindowListener(new WindowAdapter(){
                public void windowClosing(WindowEvent e){
                    container.setEnabled(true);
                }});
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setBounds(150,150,450,300);
        
        setVisible(true);
        String path = text.getText();
        if(path!=null&&!path.equals("")){
            try{c.cd(path);
                populateTree();
                populateBrowser();                
            } catch(Exception e){
                e.printStackTrace();
                populateTree();
                populateBrowser();
            }
        } else {
            populateTree();
            populateBrowser();
        }
    }
    
    /*
     * method to populate the
     * combobox that holds the tree to browse
     * with the curent location of the sftp connection
     */
    private void populateTree(){
        try{
            for(ItemListener it:tree.getItemListeners()){
                tree.removeItemListener(it);
            }
            tree.removeAllItems();
            String [] home = c.pwd().split("/");
            tree.addItem("sftp://"+c.getSession().getHost()+"/");
            for(String s:home){
                if(!s.equals("")){
                    tree.addItem(s);
                }
            }
            tree.setSelectedIndex(tree.getItemCount()-1);
            tree.addItemListener(listener);
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    /*
     * method to populate the main window
     * with files and folders according to
     * current location of sftp connection
     */
    private void populateBrowser(){
        try{
            model.clear();
            Vector<LsEntry> vector1 = c.ls(".");
            Vector<String> vector = new Vector<String>();
            Vector<String> folders = new Vector<String>();
            Vector<String> files = new Vector<String>();
            int lssize = vector1.size();
            String current;
            for (int i = 0; i < lssize; i++) {
                if (vector1.get(i).getFilename().split("\\.").length == 0) {
                    continue;
                }
                try{
                    current = c.pwd();
                    c.cd(vector1.get(i).getFilename());
                    c.cd(current);
                    folders.add(vector1.get(i).getFilename());
                } catch (SftpException e) {
                    if (e.id == 4) {
                        files.add(vector1.get(i).getFilename());
                    }
                    else{
                       e.printStackTrace();
                   }
                }
            }
            Collections.sort(folders);
            Collections.sort(files);
            for(String s:folders){
                model.addElement(new MyLabel(s,new ImageIcon(Repository.suitaicon), SwingConstants.LEFT,0));
            }
            for(String s:files){
                model.addElement(new MyLabel(s,new ImageIcon(Repository.tcicon), SwingConstants.LEFT,1));
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    /*
     * method to replace the jtextfield
     * that was passed as a parametero to the constructor
     * with the selection of the user
     */
    public void save(){
        StringBuilder s = new StringBuilder();
        s.append("/");
        for(int i=1;i<tree.getItemCount();i++){
            s.append(tree.getItemAt(i)+"/");
        }
        s.append(tfilename.getText());
        text.setText(s.toString());
    }
    
    /*
     * initialization method
     */
    private void initComponents() {
        up = new JButton(new ImageIcon(Repository.upicon));
        main = new JPanel();
        tree = new JComboBox();
        look = new JLabel();
        filename = new JLabel();
        tfilename = new JTextField();
        cancel = new JButton("Cancel");
        open = new JButton("Save");
        jScrollPane2 = new JScrollPane();
        jScrollPane2.setAlignmentX(LEFT_ALIGNMENT);
        model = new DefaultListModel();
        browser = new JList(model);
        browser.setCellRenderer(new IconListRenderer());
        browser.setLayoutOrientation(JList.VERTICAL_WRAP);
        browser.setVisibleRowCount(-1);
        browser.setSelectionMode(ListSelectionModel.SINGLE_INTERVAL_SELECTION);
        ImageIcon failicon = null;
        try{InputStream in = MySftpBrowser.class.getResourceAsStream("Icons/fail.png"); 
            failicon  = new ImageIcon(ImageIO.read(in));}
        catch(Exception e){
            e.printStackTrace();
        }
        
        browser.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent evt) {
                if (evt.getClickCount() == 2) {
                    if(((MyLabel)browser.getSelectedValue()).getType()==0){
                        try{c.cd(browser.getSelectedValue().toString());}
                        catch(Exception e){e.printStackTrace();}
                        for(ItemListener it:tree.getItemListeners()){
                            tree.removeItemListener(it);
                        }
                        tree.addItem(browser.getSelectedValue().toString());                        
                        tree.setSelectedIndex(tree.getItemCount()-1);
                        tree.addItemListener(listener);
                        populateBrowser();
                        tfilename.setText("");
                    } else {
                        tfilename.setText(browser.getSelectedValue().toString());
                        save();
                        dispose();
                        container.setEnabled(true);
                    }
                } else {
                    tfilename.setText(browser.getSelectedValue().toString());
                }
            }
        });
        
        up.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                try{
                    StringBuilder s = new StringBuilder();
                    s.append("/");
                    for(int i=1;i<tree.getItemCount();i++){
                        s.append(tree.getItemAt(i)+"/");
                    }
                    c.cd(s.toString());
                    c.cd("..");
                    populateTree();
                    populateBrowser();
                    tfilename.setText("");
                } catch(Exception e){
                    e.printStackTrace();
                }
            }
        });
        
        listener = new ItemListener(){
            public void itemStateChanged(ItemEvent evt) {        
                if (evt.getStateChange() == ItemEvent.SELECTED) {
                    try{
                        int nr = tree.getSelectedIndex();
                        while(tree.getItemCount()>nr+1){
                            tree.removeItemAt(nr+1);
                        }
                        StringBuilder s = new StringBuilder();
                        s.append("/");
                        for(int i=1;i<tree.getItemCount();i++){
                            s.append(tree.getItemAt(i)+"/");
                        }
                        c.cd(s.toString());
                        populateTree();
                        populateBrowser();
                        tfilename.setText("");
                    } catch(Exception e){
                        e.printStackTrace();
                    }
                } 
            }
        };
        
        tree.addItemListener(listener);
        look.setFont(new java.awt.Font("Tahoma", 1, 12));
        look.setText("Look in:");

        filename.setFont(new java.awt.Font("Tahoma", 1, 12));
        filename.setText("File name:");

        cancel.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                dispose();
                container.setEnabled(true);
            }
        });

        open.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                save();
                dispose();
                container.setEnabled(true);
            }
        });

        browser.setBackground(new java.awt.Color(255, 255, 255));
        jScrollPane2.setViewportView(browser);

        GroupLayout layout = new GroupLayout(main);
        main.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane2)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(filename)
                        .addPreferredGap(ComponentPlacement.RELATED)
                        .addComponent(tfilename))
                    .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addGap(0, 0, Short.MAX_VALUE)
                        .addComponent(open)
                        .addPreferredGap(ComponentPlacement.RELATED)
                        .addComponent(cancel))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(look)
                        .addPreferredGap(ComponentPlacement.RELATED)
                        .addComponent(tree, GroupLayout.PREFERRED_SIZE, 251, GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(up,30,30,30)
                        .addGap(0, 105, Short.MAX_VALUE)))
                .addContainerGap())
        );

        layout.linkSize(SwingConstants.HORIZONTAL, new Component[] {cancel, open});

        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(look)
                    .addComponent(tree, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(up, 25, 25, 25))
                .addPreferredGap(ComponentPlacement.RELATED)
                .addComponent(jScrollPane2, GroupLayout.DEFAULT_SIZE, 165, Short.MAX_VALUE)
                .addPreferredGap(ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(filename)
                    .addComponent(tfilename, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(cancel)
                    .addComponent(open))
                .addGap(12, 12, 12))
        );
    }
}

/*
 * my implementation of a DefaultListCellRenderer
 * to represent folders and files in main browser
 */
class IconListRenderer extends DefaultListCellRenderer {
    EmptyBorder border = new EmptyBorder(2,3,2,3);

    public Component getListCellRendererComponent(JList list, Object value, int index,
                                                  boolean isSelected, boolean cellHasFocus) {
        JLabel label = (JLabel) super.getListCellRendererComponent(list, value, 
                                                                   index, isSelected,
                                                                   cellHasFocus);
        label.setIcon(((JLabel)value).getIcon());
        label.setBorder(border);
        return label;
    }
}

/*
 * my implementation of jlabel to hold the
 * type of jlabel(folder or file) and icon
 */
class MyLabel extends JLabel{
    private int type;
    //0 folder , 1 file;
    public MyLabel(String text, ImageIcon icon, int i, int type){
        super(text,icon,i);
        this.type = type;
    }
    
    public int getType(){
        return this.type;
    }
    
    public String toString(){
        return this.getText();
    }
}