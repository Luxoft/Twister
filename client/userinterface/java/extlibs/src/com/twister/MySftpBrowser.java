package com.twister;
/*
File: MySftpBrowser.java ; This file is part of Twister.
Version: 2.009
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



import javax.swing.GroupLayout.Alignment;
import javax.swing.AbstractAction;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.JComboBox;

import java.awt.Component;
import java.awt.KeyEventDispatcher;
import java.awt.KeyboardFocusManager;

import javax.swing.DefaultListCellRenderer;
import javax.swing.ImageIcon;
import java.awt.Image;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;

//import com.jcraft.jsch.Channel;

import javax.imageio.ImageIO;
import javax.swing.SwingConstants;
import javax.swing.ListSelectionModel;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumn;

import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
//import com.jcraft.jsch.ChannelSftp;
import javax.swing.GroupLayout;
import javax.swing.LayoutStyle.ComponentPlacement;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

//import java.text.DateFormat;
//import java.text.SimpleDateFormat;
//import java.util.Date;
import java.util.HashMap;
//import java.util.Properties;
//import java.util.Vector;
//import com.jcraft.jsch.ChannelSftp.LsEntry;
//import com.jcraft.jsch.JSch;
//import com.jcraft.jsch.Session;
import java.util.Collections;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.Container;

public class MySftpBrowser extends JFrame {
	private static final long serialVersionUID = 1L;
	private JPanel main;
	private JButton cancel, open;
	private JLabel filename;
	private JScrollPane jScrollPane2;
	private JLabel look;
	private JTextField tfilename;
	private JComboBox tree;
	//private ChannelSftp c;
	private JButton up;
	private JTextField text;
	private ItemListener listener;
	private Container container;
	private Image suitaicon, tcicon, upicon;
	private boolean visible;
	//private Session session;
	private JCheckBox author = new JCheckBox("author");
	private JCheckBox group = new JCheckBox("group");
	private JCheckBox date = new JCheckBox("date");
	private JCheckBox size = new JCheckBox("size");
	private JTable table;
	private boolean onlyfolders;
	private AbstractAction action;//action to perform on open button trigger
	private XmlRpcClient client;
	private String currentlocation;//location on server to modify and pass to different methods
	private String host;//server host 

	/*
	 * c - SFTP connection initialized in repository text - the jtextfield that
	 * holds the path container - the parent for sftp browser
	 */
	public MySftpBrowser(String host, String user, String passwd, String port,
			JTextField text, final Container container, boolean onlyfolders) {
		this.onlyfolders = onlyfolders;
		this.text = text;
		this.container = container;
		this.host = host;
		author.setSelected(true);
		group.setSelected(true);
		date.setSelected(true);
		size.setSelected(true);
		//initializeSftp(user, host, passwd);
		initializeRPC(user, host, passwd, port);
		currentlocation = getUserHome();
		getIcons();
		initComponents();
		add(main);
		setAlwaysOnTop(true);
		try {
			container.setEnabled(false);
		} catch (Exception e) {
			e.printStackTrace();
		}
		author.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				TableColumn col = table.getColumnModel().getColumn(1);
				columnSwitch(col,author.isSelected());
			}
		});
		group.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				TableColumn col = table.getColumnModel().getColumn(2);
				columnSwitch(col,group.isSelected());
			}
		});
		date.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				TableColumn col = table.getColumnModel().getColumn(4);
				columnSwitch(col,date.isSelected());
			}
		});
		size.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				TableColumn col = table.getColumnModel().getColumn(3);
				columnSwitch(col,size.isSelected());
			}
		});
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				try {
					container.setEnabled(true);
				} catch (Exception ex) {
					ex.printStackTrace();
				}
				visible = false;
				//c.quit();
				//c.disconnect();
				//session.disconnect();
				dispose();
			}
		});
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		setBounds(150, 150, 650, 300);
		setVisible(true);
		visible = true;
		String path;
		try {
			path = text.getText();
		} catch (Exception e) {
			path = "/";
		}
		if (path != null && !path.equals("")) {
			try {
				currentlocation = path;
				//c.cd(path);
				populateTree();
				populateBrowser();
			} catch (Exception e) {
				e.printStackTrace();
				populateTree();
				populateBrowser();
			}
		} else {
			populateTree();
			populateBrowser();
		}
	}
	
	public void setButtonText(String text){
		open.setText(text);
	}
	
	private void columnSwitch(TableColumn col, boolean enable){
		if(!enable){
			col.setMinWidth(0);
			col.setMaxWidth(0);
			col.setWidth(0);
		} else {
			col.setMinWidth(0);
			col.setMaxWidth(1000);
			col.setWidth(100);
			col.setPreferredWidth(100);
		}
	}
	
	/*
     * XmlRpc main connection used by Twister framework
     */
    public void initializeRPC(String user, String host, String passwd, String port){
        try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
            configuration.setBasicPassword(passwd);
            configuration.setBasicUserName(user);
            configuration.setServerURL(new URL("http://"+user+":"+passwd+"@"+host+
                                        ":"+port+"/"));
            client = new XmlRpcClient();
            client.setConfig(configuration);
            System.out.println("Client initialized: "+client);}
        catch(Exception e){System.out.println("Could not conect to "+
                            host+" :"+port+
                            "for RPC client initialization");}
    }

//	/*
//	 * method to initialize sftp connection used to browse server
//	 */
//	private void initializeSftp(String user, String host, String passwd) {
//		try {
//			JSch jsch = new JSch();
//			session = jsch.getSession(user, host, 22);
//			session.setPassword(passwd);
//			Properties config = new Properties();
//			config.put("StrictHostKeyChecking", "no");
//			session.setConfig(config);
//			session.connect();
//			Channel channel = session.openChannel("sftp");
//			channel.connect();
//			c = (ChannelSftp) channel;
//		} catch (Exception e) {
//			e.printStackTrace();
//		}
//	}

	/*
	 * method to initialize icons used in browser window
	 */
	private void getIcons() {
		try {
			InputStream in = getClass().getResourceAsStream("suita.png");
			suitaicon = new ImageIcon(ImageIO.read(in)).getImage();
			in = MySftpBrowser.class.getResourceAsStream("tc.png");
			tcicon = new ImageIcon(ImageIO.read(in)).getImage();
			in = MySftpBrowser.class.getResourceAsStream("up.png");
			upicon = new ImageIcon(ImageIO.read(in)).getImage();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/*
	 * method to populate the combobox that holds the tree to browse with the
	 * curent location of the sftp connection
	 */
	private void populateTree() {
		try {
			for (ItemListener it : tree.getItemListeners()) {
				tree.removeItemListener(it);
			}
			tree.removeAllItems();
			//String[] home = c.pwd().split("/");
			String[] home = currentlocation.split("/");
			//tree.addItem("sftp://" + c.getSession().getHost() + "/");
			tree.addItem("sftp://" + host + "/");
			for (String s : home) {
				if (!s.equals("")) {
					tree.addItem(s);
				}
			}
			tree.setSelectedIndex(tree.getItemCount() - 1);
			tree.addItemListener(listener);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/*
	 * method to populate the main window with files and folders according to
	 * current location of sftp connection
	 */
//	private void populateBrowser() {
//		try {
//			DefaultTableModel model = (DefaultTableModel)table.getModel();
//			model.setRowCount(0);
//			Vector<LsEntry> vector1 = c.ls(".");
//			Vector<LsEntry> folders = new Vector<LsEntry>();
//			Vector<LsEntry> files = new Vector<LsEntry>();
//			int lssize = vector1.size();
//			if(lssize==2)return;
//			for (int i = 0; i < lssize; i++) {
//				if (vector1.get(i).getFilename().split("\\.").length == 0) {
//					continue;
//				}
//				if(vector1.get(i).getAttrs().isDir()){
//					folders.add(vector1.get(i));
//				} else {
//					files.add(vector1.get(i));
//				}
//			}
//			Collections.sort(folders);
//			Collections.sort(files);
//			long d;
//			DateFormat format = new SimpleDateFormat("yyyy.MM.dd HH:mm:ss");
//			Date date;
//			String data [], user, group;
//			for (LsEntry s : folders) {
//				d= s.getAttrs().getMTime();
//				d*=1000;
//				date = new Date(d);
//				data = s.getLongname().split("\\s+");
//				user = data[2];
//				group = data [3];
//				model.addRow(new Object[] {
//						new MyLabel(s.getFilename(), null,
//								SwingConstants.LEFT, 0),
//						new MyLabel(user, null,
//								SwingConstants.LEFT, 2),
//						new MyLabel(group, null,
//								SwingConstants.LEFT, 2),
//								0l
//						,
//						new MyLabel(format.format(date), null,
//								SwingConstants.LEFT, 2), });
//			}
//			if(!onlyfolders){
//				for (LsEntry s : files) {
//					d= s.getAttrs().getMTime();
//					d*=1000;
//					date = new Date(d);
//					
//					data = s.getLongname().split("\\s+");
//					user = data[2];
//					group = data [3];
//					
//					model.addRow(new Object[] {
//							new MyLabel(s.getFilename(), null,
//									SwingConstants.LEFT, 1),
//							new MyLabel(user, null,
//									SwingConstants.LEFT, 2),
//							new MyLabel(group, null,
//									SwingConstants.LEFT, 2),
////							new MyLabel(s.getAttrs().getSize() + "", null,
////									SwingConstants.LEFT, 2)
//									s.getAttrs().getSize(),
//							new MyLabel(format.format(date), null,
//									SwingConstants.LEFT, 2), });
//				}
//			}
//			model.fireTableDataChanged();
//			table.revalidate();
//			table.repaint();
//		} catch (Exception e) {
//			e.printStackTrace();
//		}
//	}
	
	//get user home on server
	private String getUserHome(){
		Object ob;
		try {
			ob = client.execute("getUserHome", new Object[]{});
			if(ob.toString().indexOf("*ERROR*")!=-1){
	            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,this,"ERROR", ob.toString());
	            return "";
	        }
			return ob.toString();
		} catch (XmlRpcException e) {
			e.printStackTrace();
			return "";
		}
        
	}
	
	
	/*
	 * method to populate the main window with files and folders according to
	 * current location of sftp connection
	 */
	private void populateBrowser() {
		try {
			DefaultTableModel model = (DefaultTableModel)table.getModel();
			model.setRowCount(0);
			
			
			//Vector<LsEntry> vector1 = c.ls(".");
			//Vector<LsEntry> folders = new Vector<LsEntry>();
			//Vector<LsEntry> files = new Vector<LsEntry>();
			
			Object ob =client.execute("listFiles", new Object[]{currentlocation});
            if(ob.toString().indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,this,"ERROR", ob.toString());
            }
            
            HashMap struct = (HashMap)ob;
            
            Object [] vector1 = (Object [])struct.get("children");
            if(vector1!=null&&vector1.length>0){
            	String author,group,size,date,attr[],name;
            	HashMap currentelem;
            	for(Object subchild:vector1){
            		currentelem = (HashMap)subchild;
            		attr = currentelem.get("meta").toString().split("\\|");
        			author = attr[0];
        			group = attr[1];
        			size = attr[2];
        			date = attr[3];
        			name = currentelem.get("data").toString();
            		if(currentelem.get("folder")==null){//here we have files
            			if(!onlyfolders){            					
            					model.addRow(new Object[] {
            							new MyLabel(name, null,
            									SwingConstants.LEFT, 1),
            							new MyLabel(author, null,
            									SwingConstants.LEFT, 2),
            							new MyLabel(group, null,
            									SwingConstants.LEFT, 2),
            									size,
            							new MyLabel(date, null,
            									SwingConstants.LEFT, 2), });
            			}
            		} else {//here we have folders
            			model.addRow(new Object[] {
        						new MyLabel(name, null,
        								SwingConstants.LEFT, 0),
        						new MyLabel(author, null,
        								SwingConstants.LEFT, 2),
        						new MyLabel(group, null,
        								SwingConstants.LEFT, 2),
        								0l
        						,
        						new MyLabel(date, null,
        								SwingConstants.LEFT, 2), });
            		}
                }
            	
            }
            model.fireTableDataChanged();
			table.revalidate();
			table.repaint();
			
			
			//int lssize = vector1.size();
			//if(lssize==2)return;
			//for (int i = 0; i < lssize; i++) {
			//	if (vector1.get(i).getFilename().split("\\.").length == 0) {
			//		continue;
			//	}
			//	if(vector1.get(i).getAttrs().isDir()){
			//		folders.add(vector1.get(i));
			//	} else {
			//		files.add(vector1.get(i));
			//	}
			//}
			//Collections.sort(folders);
			//Collections.sort(files);
//			long d;
//			DateFormat format = new SimpleDateFormat("yyyy.MM.dd HH:mm:ss");
//			Date date;
//			String data [], user, group;
//			for (LsEntry s : folders) {
//				d= s.getAttrs().getMTime();
//				d*=1000;
//				date = new Date(d);
//				data = s.getLongname().split("\\s+");
//				user = data[2];
//				group = data [3];
//				model.addRow(new Object[] {
//						new MyLabel(s.getFilename(), null,
//								SwingConstants.LEFT, 0),
//						new MyLabel(user, null,
//								SwingConstants.LEFT, 2),
//						new MyLabel(group, null,
//								SwingConstants.LEFT, 2),
//								0l
//						,
//						new MyLabel(format.format(date), null,
//								SwingConstants.LEFT, 2), });
//			}
//			if(!onlyfolders){
//				for (LsEntry s : files) {
//					d= s.getAttrs().getMTime();
//					d*=1000;
//					date = new Date(d);
//					
//					data = s.getLongname().split("\\s+");
//					user = data[2];
//					group = data [3];
//					
//					model.addRow(new Object[] {
//							new MyLabel(s.getFilename(), null,
//									SwingConstants.LEFT, 1),
//							new MyLabel(user, null,
//									SwingConstants.LEFT, 2),
//							new MyLabel(group, null,
//									SwingConstants.LEFT, 2),
////							new MyLabel(s.getAttrs().getSize() + "", null,
////									SwingConstants.LEFT, 2)
//									s.getAttrs().getSize(),
//							new MyLabel(format.format(date), null,
//									SwingConstants.LEFT, 2), });
//				}
//			}
//			model.fireTableDataChanged();
//			table.revalidate();
//			table.repaint();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	

	public boolean isVisible() {
		return visible;
	}
	
	
	public boolean isOnlyfolders() {
		return onlyfolders;
	}

	public void setOnlyfolders(boolean onlyfolders) {
		this.onlyfolders = onlyfolders;
	}

	public AbstractAction getAction() {
		return action;
	}

	public void setAction(AbstractAction action) {
		this.action = action;
	}

	/*
	 * method to replace the jtextfield that was passed as a parameter to the
	 * constructor with the selection of the user
	 */
	public void save() {
		if (text != null){
			StringBuilder s = new StringBuilder();
			s.append("/");
			for (int i = 1; i < tree.getItemCount(); i++) {
				s.append(tree.getItemAt(i) + "/");
			}
			s.append(tfilename.getText());
			text.setText(s.toString());
		}
		if(action!=null){
			action.actionPerformed(null);
		}
	}
	
	public void setFieldName(String name){
		filename.setText(name);	
	}

	/*
	 * initialization method
	 */
	private void initComponents() {
		up = new JButton(new ImageIcon(upicon));
		main = new JPanel();
		tree = new JComboBox();
		look = new JLabel();
		filename = new JLabel();
		tfilename = new JTextField();
		cancel = new JButton("Cancel");
		open = new JButton("Open");
		jScrollPane2 = new JScrollPane();
		jScrollPane2.setAlignmentX(LEFT_ALIGNMENT);

		up.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				try {
					StringBuilder s = new StringBuilder();
					s.append("/");
					//for (int i = 1; i < tree.getItemCount(); i++) {
					//	s.append(tree.getItemAt(i) + "/");
					//}
					for (int i = 1; i < tree.getItemCount()-1; i++) {
						s.append(tree.getItemAt(i) + "/");
					}
					currentlocation = s.toString();
					//c.cd(s.toString());
					//c.cd("..");
					populateTree();
					populateBrowser();
					tfilename.setText("");
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});

		listener = new ItemListener() {
			public void itemStateChanged(ItemEvent evt) {
				if (evt.getStateChange() == ItemEvent.SELECTED) {
					try {
						int nr = tree.getSelectedIndex();
						while (tree.getItemCount() > nr + 1) {
							tree.removeItemAt(nr + 1);
						}
						StringBuilder s = new StringBuilder();
						s.append("/");
						for (int i = 1; i < tree.getItemCount(); i++) {
							s.append(tree.getItemAt(i) + "/");
						}
						//c.cd(s.toString());
						currentlocation = s.toString();
						populateTree();
						populateBrowser();
						tfilename.setText("");
					} catch (Exception e) {
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

		cancel.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				dispose();
				visible = false;
				try {
					container.setEnabled(true);
				} catch (Exception e) {}
				//c.disconnect();
				//session.disconnect();
			}
		});

		open.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				save();
				dispose();
				visible = false;
				try {
					container.setEnabled(true);
				} catch (Exception e) {
				}
				//c.disconnect();
				//session.disconnect();
			}
		});
		
		String[] columnnames = new String[] { "Name", "Author", "Group",
				"Size", "Date" };
		Object[][] data = new Object[][] {};
		DefaultTableModel model = new DefaultTableModel(data, columnnames)
		{
			public Class getColumnClass(int columnIndex) {
				if(columnIndex==3)return Long.class;
				return MyLabel.class;
		    }
		};
		table = new JTable(model) {
			private static final long serialVersionUID = 1L;
			public boolean isCellEditable(int row, int column) {
				return false;
			}
		};
		table.setAutoCreateRowSorter(true);
		table.getTableHeader().setReorderingAllowed(false);
		jScrollPane2.setViewportView(table);
		table.setDefaultRenderer(Object.class, new MyTableCellRender());
		table.setShowGrid(false);
		table.setBackground(table.getParent().getBackground());
		table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		table.addMouseListener(new MouseAdapter() {

			@Override
			public void mouseClicked(MouseEvent ev) {

				MyLabel selected = (MyLabel) table.getValueAt(
						table.rowAtPoint(ev.getPoint()),
						0);
				if (ev.getClickCount() == 2) {
					if (selected.getType() == 0) {
						try {
							//c.cd(selected.toString());
							currentlocation += "/"+selected.toString();
						} catch (Exception e) {
							e.printStackTrace();
						}
						for (ItemListener it : tree.getItemListeners()) {
							tree.removeItemListener(it);
						}
						tree.addItem(selected.toString());
						tree.setSelectedIndex(tree.getItemCount() - 1);
						tree.addItemListener(listener);
						populateBrowser();
						tfilename.setText("");
					} else {
						tfilename.setText(selected.toString());
						save();
						container.setEnabled(true);
						dispose();
					}
				} else {
					tfilename.setText(selected.toString());
				}

			}
		});

		GroupLayout layout = new GroupLayout(main);
		main.setLayout(layout);
		layout.setHorizontalGroup(layout
				.createParallelGroup(GroupLayout.Alignment.LEADING)
				.addGroup(
						layout.createSequentialGroup()
								.addContainerGap()
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.LEADING)
												.addComponent(jScrollPane2)
												.addGroup(
														layout.createSequentialGroup()
																.addComponent(
																		filename)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		tfilename))
												.addGroup(
														GroupLayout.Alignment.TRAILING,
														layout.createSequentialGroup()
																.addGap(0,
																		0,
																		Short.MAX_VALUE)
																.addComponent(
																		open)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		cancel))
												.addGroup(
														layout.createSequentialGroup()
																.addComponent(
																		look)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		tree,
																		GroupLayout.PREFERRED_SIZE,
																		251,
																		GroupLayout.PREFERRED_SIZE)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		up, 30,
																		30, 30)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		author)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		group)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		size)
																.addPreferredGap(
																		ComponentPlacement.RELATED)
																.addComponent(
																		date)
																.addGap(0,
																		105,
																		Short.MAX_VALUE)))
								.addContainerGap()));

		layout.linkSize(SwingConstants.HORIZONTAL, new Component[] { cancel,
				open });

		layout.setVerticalGroup(layout
				.createParallelGroup(GroupLayout.Alignment.LEADING)
				.addGroup(
						layout.createSequentialGroup()
								.addContainerGap()
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.BASELINE)
												.addComponent(look)
												.addComponent(
														tree,
														GroupLayout.PREFERRED_SIZE,
														GroupLayout.DEFAULT_SIZE,
														GroupLayout.PREFERRED_SIZE)
												.addComponent(up, 25, 25, 25)
												.addGroup(
														layout.createSequentialGroup()
																.addGroup(
																		layout.createParallelGroup(
																				Alignment.BASELINE)
																				.addComponent(
																						author)
																				.addComponent(
																						group)
																				.addComponent(
																						size)
																				.addComponent(
																						date))))
								.addPreferredGap(ComponentPlacement.RELATED)
								.addComponent(jScrollPane2,
										GroupLayout.DEFAULT_SIZE, 165,
										Short.MAX_VALUE)
								.addPreferredGap(ComponentPlacement.RELATED)
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.BASELINE)
												.addComponent(filename)
												.addComponent(
														tfilename,
														GroupLayout.PREFERRED_SIZE,
														GroupLayout.DEFAULT_SIZE,
														GroupLayout.PREFERRED_SIZE))
								.addPreferredGap(ComponentPlacement.RELATED)
								.addGroup(
										layout.createParallelGroup(
												GroupLayout.Alignment.BASELINE)
												.addComponent(cancel)
												.addComponent(open))
								.addGap(12, 12, 12)));
	}

	/*
	 * my implementation of jlabel to hold the type of jlabel(folder or file)
	 * and icon
	 */
	class MyLabel extends JLabel {
		private static final long serialVersionUID = 1L;
		private int type;

		// 0 folder , 1 file , 2 text;
		public MyLabel(String text, ImageIcon icon, int i, int type) {
			super(text, icon, i);
			this.type = type;
		}

		public int getType() {
			return this.type;
		}

		public String toString() {
			return this.getText();
		}
	}

	/*
	 * my implementation of TableCellRenderer to render icons according
	 * to item type
	 */
	class MyTableCellRender extends DefaultTableCellRenderer {
		private static final long serialVersionUID = 1L;

		@Override
		public Component getTableCellRendererComponent(JTable arg0,
				Object arg1, boolean arg2, boolean arg3, int arg4, int arg5) {
			
			JLabel label = (JLabel) super.getTableCellRendererComponent(arg0,
					arg1, arg2, arg3, arg4, arg5);
			
//			System.out.println(arg1.getClass()+" - "+Long.class+" - "+arg1.getClass().equals(Long.class));
			
//			if(arg1.getClass().equals(Long.class)){
//				
//				if((Long)arg1 == 0 ){
//					label = (JLabel) super.getTableCellRendererComponent(arg0,
//							arg1, arg2, arg3, arg4, arg5);
//					label.setText("");
//					return label;
//				} else {
//					return super.getTableCellRendererComponent(arg0,
//							arg1, arg2, arg3, arg4, arg5);
//				}
//			}
//			
//			
//			
//			if(label.getText().equals("0"))label.setText("");
			if (((MyLabel) arg1).getType() == 0) {
//				label = (JLabel) super.getTableCellRendererComponent(arg0,
//						arg1, arg2, arg3, arg4, arg5);
				label.setIcon(new ImageIcon(suitaicon));
				if(!arg2)label.setBackground(arg0.getParent().getBackground());
				return label;
			} else if (((MyLabel) arg1).getType() == 1)	{
//				label = (JLabel) super.getTableCellRendererComponent(arg0,
//						arg1, arg2, arg3, arg4, arg5);
				label.setIcon(new ImageIcon(tcicon));
				if(!arg2)label.setBackground(arg0.getParent().getBackground());
				return label;
			} else{
//				label = (JLabel)super.getTableCellRendererComponent(arg0,
//						arg1, arg2, arg3, arg4, arg5);
				label.setIcon(null);
				if(!arg2)label.setBackground(arg0.getParent().getBackground());
				return label;
			}	
		}
	}
}