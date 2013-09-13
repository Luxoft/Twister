/*
File: Scheduler.java ; This file is part of Twister.
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
import java.applet.Applet;
import java.awt.Color;
import java.awt.Component;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Point;
import java.awt.RenderingHints;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Locale;
import java.util.Properties;

import javax.imageio.ImageIO;
import javax.swing.BorderFactory;
import javax.swing.DefaultListCellRenderer;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSpinner;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SpinnerDateModel;
import javax.swing.SpinnerModel;
import javax.swing.border.BevelBorder;
import javax.swing.plaf.basic.BasicComboBoxUI;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumn;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.toedter.calendar.JDateChooser;
import com.toedter.calendar.JTextFieldDateEditor;
import com.twister.CustomDialog;
import com.twister.Item;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Result;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

public class Scheduler extends BasePlugin implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;  
	private JPanel p;
	public XmlRpcClient client;
	private ChannelSftp c;
	private JLabel left,right,add,remove,modify,tick;
	private Calendar calendar ;
	private Icon left0,left1,right0,right1,add0,add1,
				 remove0,remove1,modify0,modify1,backgroundim,
				 ok0,ok1,cancel0,cancel1;
	private MyCalendar mycalendar;
	private ArrayList schedules [] = new ArrayList[31];
	private JTable jTable1;
	private int initialx, initialy;
	
	
	/*
	 * method used local
	 */
	public static void main(String [] args){
		try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
	    	configuration.setServerURL(new URL("http://11.126.32.14:88/"));
	    	XmlRpcClient client = new XmlRpcClient();
	    	client.setConfig(configuration);
	    	Scheduler sch = new Scheduler();
	    	sch.setRPC(client);
	    	sch.init(null, null, null, null,null);
			JFrame f = new JFrame();
			f.add(sch.getContent());
			f.setVisible(true);
			f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			f.setBounds(100,100,900,700);
	    	System.out.println("Client initialized: "+client);
		}
		catch(Exception e){System.out.println("Could not conect to "+
						"http://11.126.32.14:88 for RPC client initialization");
						e.printStackTrace();
		}
	}
	
	public void setRPC(XmlRpcClient client){
		this.client = client;
	}

	
	/*
	 * main initialization method
	 */
	@Override
	public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
			final Hashtable<String, String> variables,final Document pluginsConfig,Applet container) {
		super.init(suite, suitetest, variables,pluginsConfig,container);
		System.out.println("Initializing "+getName()+" ...");
		calendar = Calendar.getInstance();
		//initializeSFTP();
		initializeRPC();
		p = new JPanel(){
			private static final long serialVersionUID = 1L;
			public void paint(Graphics g){
				super.paint(g);
				drawDate(g);
			}
		};
		initMainPanel();
		updateSchedules();
        //createXMLStructure();
        System.out.println(getName()+" initialized");
	}
	
	public void initMainPanel(){
		JPanel panel1 = new JPanel();
		JScrollPane jScrollPane1 = new JScrollPane();
		jScrollPane1.setBounds(54,469,694,105);
		jScrollPane1.setBorder(null);
		jTable1 = new JTable();
		jTable1.getTableHeader().setReorderingAllowed(false);
		panel1.setLayout(null);
        panel1.setMaximumSize(new Dimension(800, 600));
        panel1.setMinimumSize(new Dimension(800, 600));
        panel1.setPreferredSize(new Dimension(800, 600));
        mycalendar = new MyCalendar(calendar,jTable1);
		mycalendar.setBounds(65, 85, 667, 300);
		try {
			InputStream in = getClass().getResourceAsStream("schedulerbackground.png");
			Image im = ImageIO.read(in);
			ImageIcon icon = new ImageIcon(im);
	        JLabel background = new JLabel(icon);
	        background.setBounds(0, 0, 800, 600);
	        in = getClass().getResourceAsStream("modify0.png");
			im = ImageIO.read(in);
			modify0 = new ImageIcon(im);			
			in = getClass().getResourceAsStream("modify1.png");
			im = ImageIO.read(in);
			modify1 = new ImageIcon(im);			
			modify = new JLabel(modify0);
			modify.addMouseListener(new MouseAdapter() {
				public void mouseEntered(MouseEvent ev){
					modify.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
				}
				public void mousePressed(MouseEvent ev){
					modify.setIcon(modify1);
				}
				public void mouseReleased(MouseEvent ev){
					modify.setIcon(modify0);
					scheduleWindow(true);
				}
			});
			modify.setBounds(337, 393, 123, 32);
			in = getClass().getResourceAsStream("remove0.png");
			im = ImageIO.read(in);
			remove0 = new ImageIcon(im);
			remove = new JLabel(remove0);			
			in = getClass().getResourceAsStream("remove1.png");
			im = ImageIO.read(in);
			remove1 = new ImageIcon(im);			
			remove.addMouseListener(new MouseAdapter() {
				public void mouseEntered(MouseEvent ev){
					remove.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
				}
				public void mousePressed(MouseEvent ev){
					remove.setIcon(remove1);
				}
				public void mouseReleased(MouseEvent ev){
					remove.setIcon(remove0);
					removeSchedule();
				}
			});
			remove.setBounds(540, 393, 127, 26);
			in = getClass().getResourceAsStream("add0.png");
			im = ImageIO.read(in);
			add0 = new ImageIcon(im);			
			in = getClass().getResourceAsStream("add1.png");
			im = ImageIO.read(in);
			add1 = new ImageIcon(im);			
			add = new JLabel(add0);
			add.addMouseListener(new MouseAdapter() {
				public void mouseEntered(MouseEvent ev){
					add.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
				}
				public void mouseExited(MouseEvent ev){
				}
				public void mousePressed(MouseEvent ev){
					add.setIcon(add1);
				}
				public void mouseReleased(MouseEvent ev){
					add.setIcon(add0);
					scheduleWindow(false);
				}
			});
			add.setBounds(150, 393, 81, 26);
			in = getClass().getResourceAsStream("btn0.png");
			im = ImageIO.read(in);
			right0 = new ImageIcon(im);			
			in = getClass().getResourceAsStream("btn1.png");
			im = ImageIO.read(in);
			right1 = new ImageIcon(im);	
			right = new JLabel(right0);
			right.addMouseListener(new MouseAdapter() {
				public void mouseEntered(MouseEvent ev){
					right.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
				}
				public void mousePressed(MouseEvent ev){
					right.setIcon(right1);
				}
				public void mouseReleased(MouseEvent ev){
					right.setIcon(right0);
					calendar.add(Calendar.MONTH, 1);
					calendar.set(Calendar.DAY_OF_MONTH, 1);
					String dayname = new SimpleDateFormat("EEEE",Locale.US).
										format(calendar.getTime()).toLowerCase();
					mycalendar.days.setDays(calendar.getActualMaximum(Calendar.DAY_OF_MONTH),dayname);
					updateSchedules();
					p.repaint();
					mycalendar.days.clearTable();
				}
			});
			right.setBounds(480, 30, 28, 28);
			in = getClass().getResourceAsStream("lbtn0.png");
			im = ImageIO.read(in);
			left0 = new ImageIcon(im);
			in = getClass().getResourceAsStream("lbtn1.png");
			im = ImageIO.read(in);
			left1 = new ImageIcon(im);
			left = new JLabel(left0);
			left.addMouseListener(new MouseAdapter() {
				public void mouseEntered(MouseEvent ev){
					left.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
				}
				public void mouseExited(MouseEvent ev){
				}
				public void mousePressed(MouseEvent ev){
					left.setIcon(left1);
				}
				public void mouseReleased(MouseEvent ev){
					left.setIcon(left0);
					calendar.add(Calendar.MONTH, -1);
					calendar.set(Calendar.DAY_OF_MONTH, 1);
					String dayname = new SimpleDateFormat("EEEE",Locale.US).
										format(calendar.getTime()).toLowerCase();
					mycalendar.days.setDays(calendar.getActualMaximum(Calendar.DAY_OF_MONTH),dayname);
					updateSchedules();
					p.repaint();
					mycalendar.days.clearTable();
				}
			});
			left.setBounds(282, 30, 28, 28);
						
			in = getClass().getResourceAsStream("windowback.png");
			im = ImageIO.read(in);
			backgroundim = new ImageIcon(im);
			
			in = getClass().getResourceAsStream("tick.png");
			im = ImageIO.read(in);
			Icon image = new ImageIcon(im);
			tick = new JLabel(image);
			tick.setBounds(53,250,17,14);
			
			in = getClass().getResourceAsStream("ok0.png");
			im = ImageIO.read(in);
			ok0 = new ImageIcon(im);
			
			in = getClass().getResourceAsStream("ok1.png");
			im = ImageIO.read(in);
			ok1 = new ImageIcon(im);
			
			in = getClass().getResourceAsStream("cancel0.png");
			im = ImageIO.read(in);
			cancel0 = new ImageIcon(im);
			
			in = getClass().getResourceAsStream("cancel1.png");
			im = ImageIO.read(in);
			cancel1 = new ImageIcon(im);
			
			tick = new JLabel(image);
			tick.setBounds(53,250,17,14);
			
			
			panel1.add(mycalendar);
			panel1.add(right);
			panel1.add(left);
			panel1.add(add);
			panel1.add(remove);
			panel1.add(modify);
	        panel1.add(jScrollPane1);
	        panel1.add(background);
	        
		} catch (IOException e) {
			e.printStackTrace();
		}

        jTable1.setModel(new DefaultTableModel(
            new Object [][] {},
            new String [] {"Project","Date","Hour",
            			   "Force","Time Limit",
            			   "Description","User",""}){
			private static final long serialVersionUID = 1L;
			public boolean isCellEditable(int row, int col){
        		return false;  
        }});
        
        TableColumn column = jTable1.getColumnModel().getColumn(7);
        column.setMaxWidth(0);
        column.setMinWidth(0);
        column.setPreferredWidth(0);
        column.setWidth(0);
        jScrollPane1.setViewportView(jTable1);
        p.add(panel1);
	}
	
	/*
	 * method used for creation and
	 * initialization of the window
	 * on adding or modifying a schedule
	 */
	public void scheduleWindow(final boolean modify){		
		final JFrame f = new JFrame();
		final JPanel panel = new JPanel();
		
		JLabel project = new JLabel("Project:");
		project.setBounds(10, 10, 48, 20);
		//implementing drag behavior
		panel.addMouseMotionListener(new MouseAdapter() {			
			public void mouseDragged(MouseEvent arg0) {
				int X = initialx-arg0.getX();
				int Y = initialy-arg0.getY();
				Point p = f.getLocation();
				f.setLocation(p.x-X, p.y-Y);
				initialx = arg0.getX()+X;
				initialy = arg0.getY()+Y;
			}
			public void mouseMoved(MouseEvent arg0) {
				initialx = arg0.getX();
				initialy = arg0.getY();
			}
		});
		
		
		try{c.cd(variables.get("remoteusersdir"));
		}
        catch(Exception e){
            System.out.println("Could not get to "+
            					variables.get("remoteusersdir")+
            					"on sftp");}
        int size ;
        try{size= c.ls(variables.get("remoteusersdir")).size();
        	}
        catch(Exception e){
            System.out.println("No suites xml");
            size=0;}
        ArrayList<String> files = new ArrayList<String>();
        String name=null;
        for(int i=0;i<size;i++){
            try{name = ((LsEntry)c.ls(variables.get("remoteusersdir")).get(i)).getFilename();
                if(name.split("\\.").length==0)continue; 
                if(name.toLowerCase().indexOf(".xml")==-1)continue;
                if(name.equals("last_edited.xml"))continue;
                files.add(name.toString());
            }
            catch(Exception e){
                e.printStackTrace();}
        }   
        String users[] = new String[files.size()];
        for(int i=0;i<files.size();i++){
            users[i] = files.get(i);
        }
		final JComboBox<String> tproject = new JComboBox<String>(users);
		tproject.setUI(new BasicComboBoxUI());
		tproject.setBounds(76,10,140,23);
		tproject.setRenderer(new DefaultListCellRenderer() {
		    @Override
		    public void paint(Graphics g) {
		        setBackground(Color.WHITE);
		        setForeground(Color.BLACK);
		        super.paint(g);
		    }
		});
		
		panel.add(tproject);
		
		final JLabel date = new JLabel();
		date.setBounds(76, 179, 100, 20);
		final JDateChooser tdate = new JDateChooser();
		((JTextFieldDateEditor)tdate.getDateEditor()).addPropertyChangeListener(new PropertyChangeListener() {
			@Override
			public void propertyChange(PropertyChangeEvent arg0) {
				if(arg0.getPropertyName().equals("date")){
					String [] form = (((JTextFieldDateEditor)tdate.getDateEditor()).getText()).split("\\.");
					StringBuilder sb = new StringBuilder();
					for(int i=form.length-1;i>-1;i--){
						sb.append(form[i]);
						sb.append("-");
					}
					sb.deleteCharAt(sb.length()-1);
					date.setText(sb.toString());
				}
			}
		});
		tdate.getCalendar();
		tdate.setBounds(160,178,22,22);
		panel.add(date);
		panel.add(tdate);
		panel.addMouseListener(new MouseAdapter(){
			public void mouseReleased(MouseEvent ev){
				int x = ev.getX();
				int y = ev.getY();
				if(x>54&&x<69&&y>250&&y<265){
					tick.setVisible(!tick.isVisible());
				}
			}
		});
		
		
		SpinnerModel model = new SpinnerDateModel();
		final JSpinner timeSpinner = new JSpinner(model);
		timeSpinner.setBorder(null);
		JComponent editor = new JSpinner.DateEditor(timeSpinner, "HH:mm:ss");
		timeSpinner.setEditor(editor);
		timeSpinner.setBounds(121,40,95,23);
		panel.add(timeSpinner);
		
		final JTextField tlimit = new JTextField();
		tlimit.setBounds(78,216,70,22);
		tlimit.setBorder(null);
		panel.add(tlimit);
		final JTextArea tdesc = new JTextArea();
		tdesc.setWrapStyleWord(true);
		tdesc.setLineWrap(true);
		JScrollPane scroll = new JScrollPane(tdesc);
		scroll.setBorder(null);
		scroll.setBounds(5,96,210,45);
		panel.add(scroll);
		final JComboBox<String> ttype = new JComboBox<String>(new String[]{"onetime","daily","weekley"});
		ttype.setBounds(125,144,90,21);
		ttype.setUI(new BasicComboBoxUI());
		ttype.setRenderer(new DefaultListCellRenderer() {
		    @Override
		    public void paint(Graphics g) {
		        setBackground(Color.WHITE);
		        setForeground(Color.BLACK);
		        super.paint(g);
		    }
		});
		
		ttype.setBackground(Color.WHITE);
		ttype.addItemListener(new ItemListener() {
			
			@Override
			public void itemStateChanged(ItemEvent arg0) {
				if(arg0.getStateChange()==ItemEvent.SELECTED &&
				   arg0.getItem().toString().equals("daily")){
					tdate.setEnabled(false);
					date.setText("");
				} else {
					tdate.setEnabled(true);
				}
				
			}
		});
		panel.add(ttype);
		
		panel.setLayout(null);
		panel.setBounds(0,0,615,30);
		panel.setBorder(BorderFactory.createBevelBorder(BevelBorder.RAISED));
		f.add(panel);
		f.setUndecorated(true);
		f.setLayout(null);
		f.setVisible(true);
		f.setAlwaysOnTop(true);
		if(modify){
			if(jTable1.getSelectedRow()!=-1){
				int row = jTable1.getSelectedRow();
				String cproject =jTable1.getModel().getValueAt(row, 0).toString();
				String cdate =jTable1.getModel().getValueAt(row, 1).toString();
				String chour =jTable1.getModel().getValueAt(row, 2).toString();
				String cforce = jTable1.getModel().getValueAt(row, 3).toString();
				String ctimelimit = jTable1.getModel().getValueAt(row, 4).toString();
				String cdescription =jTable1.getModel().getValueAt(row, 5).toString();
				String [] s = cproject.split("/");
				cproject = s[s.length-1];
				for(int i=0;i<tproject.getItemCount();i++){
					if(tproject.getItemAt(i).equals(cproject)){
						tproject.setSelectedIndex(i);
						break;
					}
				}
				date.setText(cdate);
				((JSpinner.DefaultEditor) timeSpinner.getEditor()).getTextField().setText(chour);
				tick.setVisible(Boolean.parseBoolean(cforce));
				tlimit.setText(ctimelimit);
				tdesc.setText(cdescription);
			}else {
				JOptionPane.showMessageDialog(p, "Please select a row from schedules to modify");
				f.dispose();
			}
		}
		
		panel.add(tick);
		final JLabel cancel = new JLabel(cancel0);
		cancel.setBounds(122,277,87,22);
        panel.add(cancel);
        cancel.addMouseListener(new MouseAdapter(){
        	public void mouseEntered(MouseEvent ev){
        		cancel.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
			}
        	public void mouseReleased(MouseEvent ev){
        		f.dispose();
        	}
        	public void mousePressed(MouseEvent ev){
        		cancel.setIcon(cancel1);
        	}
        });
        
        final JLabel okbtn = new JLabel(ok0);
        okbtn.setBounds(30,277,87,22);
        panel.add(okbtn);
        okbtn.addMouseListener(new MouseAdapter(){
        	
        	public void mouseEntered(MouseEvent ev){
        		okbtn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
			}
        	
        	public void mousePressed(MouseEvent ev){
        		okbtn.setIcon(ok1);
        	}
        	
        	public void mouseReleased(MouseEvent ev){
        		String selectedproject = variables.get("remoteusersdir")+
        								"/"+tproject.getSelectedItem().toString();
				String selecteddate = date.getText();
				String selectedhour = ((JSpinner.DefaultEditor) timeSpinner.getEditor()).
																getTextField().getText();
				String isforced ;
				if(tick.isVisible()){
					isforced = "1";
				} else {
					isforced = "0";
				}
				String type = ttype.getSelectedItem().toString();
				
				if(type.equals("daily")){
					selecteddate = "";
				} else if(type.equals("weekley")){
					String []st = selecteddate.split("-");
					if(st.length==3){
						Calendar temp = Calendar.getInstance();
						temp.set(Calendar.YEAR, Integer.parseInt(st[0]));
						temp.set(Calendar.MONTH, Integer.parseInt(st[1])-1);
						temp.set(Calendar.DAY_OF_MONTH, Integer.parseInt(st[2]));
						selecteddate = new SimpleDateFormat("EEEE",Locale.US).
											format(temp.getTime()).toLowerCase();
						StringBuilder sb = new StringBuilder();
						sb.append(Character.toUpperCase(selecteddate.charAt(0)));
						sb.append(selecteddate.substring(1));
						selecteddate = sb.toString();
					}
				}
				
				String selectedlimit = tlimit.getText();
				String selecteddesc = tdesc.getText();
				String user = variables.get("user");
				HashMap<String, String> hash = new HashMap<String, String>();
				hash.put("project-file", selectedproject);
				if(selecteddate.equals("")){
					hash.put("date-time", selectedhour);
				} else {
					hash.put("date-time", selecteddate+" "+selectedhour);
				}
				hash.put("force", isforced);
				hash.put("time-limit", selectedlimit);
				hash.put("description", selecteddesc);
				String st="";
				try {
					if(modify){
						int row = jTable1.getSelectedRow();
						String key = jTable1.getModel().getValueAt(row, 7).toString();
						st = client.execute("Change",new Object[]{key,hash}).toString();
						updateSchedules();
						p.repaint();
					} else {
						st = client.execute("Add",new Object[]{user,hash}).toString();
						updateSchedules();
						p.repaint();
					}
					mycalendar.days.updateSelectedDay(mycalendar.days.getSelectedDaynr());
				} catch (XmlRpcException e) {
					e.printStackTrace();
					st = "false";
				}
				f.dispose();
				System.out.println(st);
				if(st.indexOf("*ERROR*")!=-1){
					JOptionPane.showMessageDialog(p, "There was an error in adding the schedule: "+"\n"+st);
				}
        	}
        });
		
		JLabel background = new JLabel(backgroundim);
        background.setBounds(0, 0, 220, 308);
        panel.add(background);
        
		Point point = jTable1.getLocationOnScreen();
		f.setBounds(point.x+200,point.y-210,220,308);
		panel.setBounds(0, 0,220,308);
		panel.setBackground(new Color(220,220,220));
	}
	
	/*
	 * displays a list of project files
	 * and inserts the name of the selected one
	 * into the field
	 */
	public void openProjectFile(JTextField field){
		try{c.cd(variables.get("remoteusersdir"));}
        catch(Exception e){
            System.out.println("Could not get to "+variables.get("remoteusersdir")+"on sftp");}
        int size ;
        try{size= c.ls(variables.get("remoteusersdir")).size();}
        catch(Exception e){
            System.out.println("No suites xml");
            size=0;}
        ArrayList<String> files = new ArrayList<String>();
        String name=null;
        for(int i=0;i<size;i++){
            try{name = ((LsEntry)c.ls(variables.get("remoteusersdir")).get(i)).getFilename();
                if(name.split("\\.").length==0)continue; 
                if(name.toLowerCase().indexOf(".xml")==-1)continue;
                if(name.equals("last_edited.xml"))continue;
                files.add(name.toString());
            }
            catch(Exception e){
                e.printStackTrace();}
        }   
        String users[] = new String[files.size()];
        for(int i=0;i<files.size();i++){
            users[i] = files.get(i);
        }
        JComboBox <String>combo = new JComboBox<String>(users);
        
        int resp = (Integer)CustomDialog.showDialog(combo,
                            JOptionPane.INFORMATION_MESSAGE,
                            JOptionPane.OK_CANCEL_OPTION,Scheduler.this,
                            "Project File",null);
        
        if(resp==JOptionPane.OK_OPTION){
            String user = combo.getSelectedItem().toString();
            field.setText(variables.get("remoteusersdir")+"/"+user);
        }
	}
	
	/*
	 * method to remove a schedule 
	 * based on selected row
	 */
	public void removeSchedule(){
		if(jTable1.getSelectedRow()!=-1){
			int row = jTable1.getSelectedRow();
			try {
				String s = client.execute("Delete",new Object[]{"tscguest",
																jTable1.getModel().getValueAt(row, 7)}).toString();
				if(Boolean.parseBoolean(s)){
					updateSchedules();
					mycalendar.days.updateSelectedDay(mycalendar.days.getSelectedDaynr());
				}
			} catch (XmlRpcException e) {
				e.printStackTrace();
			}
		}else {
			JOptionPane.showMessageDialog(p, "Please select a row from schedules to remove");
		}
	}

	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public String getFileName() {
		String filename = "Scheduler.jar";
		return filename;
	}

	@Override
	public void terminate() {
		super.terminate();
		p=null;
		client=null;
		c=null;
		left=null;
		right=null;
		add=null;
		remove=null;
		modify=null;
		calendar = null;
		left0 = null;
		left1 = null;
		right0 = null;
		right1 = null;
		add0 = null;
		add1= null;
		remove0 = null;
		remove1 = null;
		modify0 = null;
		modify1 = null;
		mycalendar=null;
		schedules = null;
		jTable1 = null;
	} 

	@Override
	public String getName() {
		String name = "Scheduler";
		return name;
	}
	
	/*
	 * method to get schedules from server
	 */
	private void updateSchedules(){
		try {
			schedules = new ArrayList[31];
			for(int i=0;i<31;i++){
				schedules[i] = new ArrayList();
			}
			Object [] s = (Object [])client.execute("List",new Object[]{""});
			for(Object ob:s){
				HashMap<String,String> hash = (HashMap<String,String>)ob;
				String date = hash.get("date-time");
				if(date.indexOf(" ")==-1){//it is daily
					for(ArrayList array:schedules){
						array.add(hash);
					}
				} else if(date.split(" ")[0].matches(".*\\d.*")){//it is one time
					String day = date.split(" ")[0];
					int  nr = Integer.parseInt(day.split("-")[2]);
					int month = Integer.parseInt(day.split("-")[1]);
					int year = Integer.parseInt(day.split("-")[0]);
					if(calendar.get(Calendar.YEAR)==year && 
					   calendar.get(Calendar.MONTH)+1==month){
						schedules[nr-1].add(hash);
					}
				} else {//it is weekley 
					Calendar c = (Calendar)calendar.clone();
					String day = date.split(" ")[0].toLowerCase();
					c.set(Calendar.DAY_OF_MONTH, 1);
					int month = c.get(Calendar.MONTH);
					while(c.get(Calendar.MONTH)==month){
						String compare = new SimpleDateFormat("EEEE",Locale.US).
											format(c.getTime()).toLowerCase();
						if(day.equals(compare)){
							schedules[c.get(Calendar.DAY_OF_MONTH)-1].add(hash);
						}
						c.add(Calendar.DAY_OF_MONTH, 1);
					}					
				}
			}
			mycalendar.days.updateSchedules(schedules);
		} catch (XmlRpcException e) {
			e.printStackTrace();
		}
	}
	
//	public void initializeSFTP(){
//		try{
//			JSch jsch = new JSch();
//            String user = variables.get("user");
//			Session session = jsch.getSession(user, variables.get("host"), 22);
//			session.setPassword(variables.get("password"));
//			Properties config = new Properties();
//            config.put("StrictHostKeyChecking", "no");
//            session.setConfig(config);
//            session.connect();
//            Channel channel = session.openChannel("sftp");
//            channel.connect();
//            c = (ChannelSftp)channel;
//            System.out.println("SFTP successfully initialized");
//		}
//		catch(Exception e){
//			System.out.println("SFTP could not be initialized");
//			e.printStackTrace();
//		}
//	}
	
	private void drawDate(Graphics g){
		StringBuilder sb = new StringBuilder();
		sb.append(new SimpleDateFormat("MMM").format(calendar.getTime()).toLowerCase());
		sb.append(" "+calendar.get(Calendar.YEAR));
		Graphics2D gr = (Graphics2D)g;
		gr.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
				RenderingHints.VALUE_ANTIALIAS_ON);
		gr.setColor(new Color(100,100,100));
		gr.setFont(new Font("Bodoni MT", Font.BOLD, 22));
		gr.drawString(sb.toString(), p.getWidth()/2-42, 55);
	}	
	
	public void initializeRPC(){
		try{
			XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
	        configuration.setServerURL(new URL("http://"+variables.get("host")+":88/"));
	        configuration.setBasicPassword(variables.get("password"));
	        configuration.setBasicUserName(variables.get("user"));
	        client = new XmlRpcClient();
	        client.setConfig(configuration);
	        System.out.println("Client initialized: "+client);}
		catch(Exception e){System.out.println("Could not conect to "+
                        variables.get("host")+" :88/");}
	}
	
	/*
     * method to copy plugins configuration file
     * to server 
     */
//    public boolean uploadPluginsFile(){
//        try{
//            DOMSource source = new DOMSource(pluginsConfig);
//            File file = new File(variables.get("pluginslocalgeneralconf"));
//            Result result = new StreamResult(file);
//            TransformerFactory transformerFactory = TransformerFactory.newInstance();
//            Transformer transformer = transformerFactory.newTransformer();
//            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
//            transformer.setOutputProperty("{http:xml.apache.org/xslt}indent-amount","4");
//            transformer.transform(source, result);
//            c.cd(variables.get("remoteuserhome")+"/twister/config/");
//            FileInputStream in = new FileInputStream(file);
//            c.put(in, file.getName());
//            in.close();
//            System.out.println("Saved "+file.getName()+" to: "+
//					variables.get("remoteuserhome")+"/twister/config/");
//            return true;}
//        catch(Exception e){
//            e.printStackTrace();
//            return false;
//        }
//    }
}
