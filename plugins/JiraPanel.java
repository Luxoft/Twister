/*
File: JiraPanel.java ; This file is part of Twister.
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
import java.awt.Rectangle;
import java.awt.Color;
import java.awt.Font;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.Insets;
import javax.swing.border.EtchedBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.JTableHeader;
import javax.swing.table.TableCellRenderer;
import javax.swing.table.TableColumn;
import javax.swing.JLabel;
import javax.swing.SwingConstants;
import java.awt.BorderLayout;
import javax.swing.JComboBox;
import java.awt.Component;
import javax.swing.Box;
import java.awt.Dimension;
import java.awt.FlowLayout;

import javax.swing.BorderFactory;
import javax.swing.DefaultComboBoxModel;
import javax.swing.DefaultListModel;
import javax.swing.JComponent;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JScrollPane;
import javax.swing.BoxLayout;
import javax.swing.JTable;
import javax.swing.JButton;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.ListSelectionModel;
import javax.swing.UIManager;

import java.awt.CardLayout;
import java.awt.GridLayout;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import com.toedter.calendar.JDateChooser;

import javax.swing.JPasswordField;
import java.io.File;


public class JiraPanel extends JPanel implements ActionListener {
	/**
	 * The JiraPanel class implements the GUI functionality for the JiraPlugin.
	 */
	private static final long serialVersionUID = 1L;
	
	// this list of fields is a sub-set of the issue fields, and contains only those fields than can be filled at issue creation
	final static String[] ISSUE_FIELD_NAMES_CREATE = {"project", "type", "priority", "status", "summary","description", 
        "environment", "components","affectsVersions","fixVersions","reporter","attachmentNames","duedate"};	

	final static String ISSUE_FIELD_ATTACHMENT = "attachmentNames";
	
	final static Font LOGIN_TITLE_FONT = new Font("Book Antiqua", Font.BOLD, 12);
	final static Font LABEL_FONT = new Font("Tahoma", Font.BOLD, 11);	
	final static Font LABEL_ITALIC_FONT = new Font("Tahoma", Font.ITALIC, 11);
	
	final static String DATE_FORMAT = "yyyy-MM-dd HH:mm:ss";
	
	final static Color TABLE_HEADER_COLOR = new Color(165,203,255);
	final static Color TABLE_ODD_ROW_COLOR = new Color(232,232,232);
	
	final static String LOGIN = "Login";
	final static String CHANGE_LOGIN = "Change Login";
	
    final static String LOGIN_PANEL = "Login";
    final static String JIRA_PANEL = "Jira";
    final static String PROJECT_SELECTED = "Project selected";
    final static String VERSION_SELECTED = "Version selected";
    final static String COMPONENT_SELECTED = "Component selected";
    
    final static String PUSH_CREATE_ISSUE_BTN = "Create new issue";
    final static String PUSH_EDIT_ISSUE_BTN = "Edit issue";
    final static String PUSH_ADD_ATTACHMENT = "Add attachment";
    final static String PUSH_SEE_COMMENT = "See comments";
    final static String PUSH_ADD_COMMENT = "Add new comment";
    final static String PUSH_SEARCH_BTN = "Search issue:";
    
    // TODO: see how to manage filtering on versions and/or components when fetching issues
    final static String COMPONENT = "component";
    final static String AFFECTS_VERSION = "affectedVersion";
    final static String FIX_VERSION = "fixVersion";
    final static String ALL_VERSION = "allVersion";
    
	private static String[] projectsDefault = { "- Select project -" };		
	private static String[] versionsDefault = { "- Select version -" };		
	private static String[] componentsDefault = { "- Select component -" };
        
	JFrame commentsPopup;
	JPanel commentsPanel;
	JFrame attachmentsPopup;
	
	JLabel lblUsername;
	JLabel lblInfo;
	
	JComboBox cbProjects;
	JComboBox cbVersions;
	JComboBox cbComponents;
	
	JTextField tfSearchIssue;
	JTextField tfUsername;
	JTextField tfJiraServer;
	JPasswordField tfPassword;
	
	JButton btnLogin;
	JButton btnChangeLogin;
	JButton btnEditIssue;
	JButton btnAddAttach;
	JButton btnSeeComments;
	
	JScrollPane scrollPane;
	MyTable issuesTable;
	
	JiraPlugin jp;
	String jiraUser;
	

	/**
	 * This method dynamically updates the contents of a ComboBox.
	 * @param c - JComboBox object to update
	 * @param values - array of String values to update the ComboBox 
	 */
	public void setComboValues(JComboBox c, String[] values){
		DefaultComboBoxModel model = new DefaultComboBoxModel(values);
		c.setModel(model);
	}	
	/**
	 * This method dynamically updates the contents of a Label.
	 * The label displays the name of the user that is currently logged into Jira. 
	 * @param username - current user (String) 
	 */
	public void setLblUsername(String username) {
		this.lblUsername.setText(username);
	}
	/**
	 * This method switches between the "login" panel and the "plugin" panel, and reverse.
	 * @param panel - the name of the panel to display (String) 
	 */
	public void showPanel(String panel){
		CardLayout cl = (CardLayout) this.getLayout();
		cl.show(this, panel);
	}
	/**
	 * The init method initializes the contents of the plugin panel after a successful login.
	 */
	public void init(){		
		setComboValues(cbVersions,versionsDefault);		
		setComboValues(cbComponents,componentsDefault);
		cbVersions.setEnabled(false);
		cbComponents.setEnabled(false);
		scrollPane.setViewportView(null);		
		tfSearchIssue.setText("");
	}
	/**
	 * This method dynamically updates the contents of the table displaying issues.
	 * @param data - data to display in the table as a list of HashMap objects
	 * @param columnNames - names of the table column as an array of String
	 * @return int value that denotes the outcome of the update  
	 */
	public int setTableModel(List data, String[] columnNames){	
		if (data==null){
			this.scrollPane.setViewportView(new JTextArea("No issues have been found."));
			btnEditIssue.setEnabled(false);
			btnAddAttach.setEnabled(false);
			btnSeeComments.setEnabled(false);
			return -1;
		}
		int nCols = columnNames.length;
		int nRows = data.size();
		Object[][] tableData = new Object[nRows][nCols];
		for (int i=0; i<nRows; i++){
			
			HashMap h = (HashMap) data.toArray()[i];
//			System.out.println(h.get("key"));
			for (int j = 0; j<nCols; j++){
//				System.out.println(columnNames[j]);
				tableData[i][j]=jp.getFieldValue(h,columnNames[j]);										
			}
		}		
		this.issuesTable = new MyTable(new MyTableModel(tableData,columnNames));
		this.issuesTable.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
		this.issuesTable.setAutoCreateRowSorter(true);
		JTableHeader header = this.issuesTable.getTableHeader();
		header.setBackground(JiraPanel.TABLE_HEADER_COLOR);
		header.setFont(JiraPanel.LOGIN_TITLE_FONT);		
		this.scrollPane.setViewportView(this.issuesTable);
		btnEditIssue.setEnabled(true);
		btnAddAttach.setEnabled(true);
		btnSeeComments.setEnabled(true);
		return 0;		
	}
	/**
	 * This method treats the user events that occur in the main GUI window.
	 * @param arg0 - the user event
	 */
	@Override
	public void actionPerformed(ActionEvent arg0) {
		int projectIndex;
		int issueIndex;
		Object selectedIssueKey;
		HashMap selectedIssue;
		lblInfo.setText("Info");
		
		System.out.println(arg0.getActionCommand()+":");
		switch (arg0.getActionCommand()){
		case LOGIN:  
			showPanel(JiraPanel.JIRA_PANEL);

			jp.JiraLogin();			

			jiraUser = tfUsername.getText();
			lblUsername.setText(jiraUser);
			
			break;
		case CHANGE_LOGIN: // return to the login panel 
			System.out.println("\t - returning to the login panel...");
			showPanel(JiraPanel.LOGIN_PANEL);
			break;
		case PROJECT_SELECTED: // fill in versions and components for the selected project
			projectIndex = cbProjects.getSelectedIndex();
			init();
			Object[] versions = jp.JiraGetVersions(projectIndex); 
			jp.setVersions(versions);
			if (jp.getJiraVersions()!=null){
				setComboValues(cbVersions,jp.getProperty(versions,"name"));
				cbVersions.setEnabled(true);
			}
			Object[] components = jp.JiraGetComponents(projectIndex);
			jp.setComponents(components);
			if (jp.getJiraComponents()!=null){
				setComboValues(cbComponents,jp.getProperty(components,"name"));
				cbComponents.setEnabled(true);
			}
			jp.JiraGetIssues(projectIndex);
			break;
		case VERSION_SELECTED: // filter issue list by the selected version
			projectIndex = cbProjects.getSelectedIndex();			
			int versionIndex = cbVersions.getSelectedIndex();			
			jp.JiraGetIssues(projectIndex,versionIndex,AFFECTS_VERSION);
			break;
		case COMPONENT_SELECTED: // filter the issue list by the selected component
			projectIndex = cbProjects.getSelectedIndex();						
			int componentIndex = cbComponents.getSelectedIndex();			
			jp.JiraGetIssues(projectIndex,componentIndex,JiraPanel.COMPONENT);
			break;	
		case PUSH_CREATE_ISSUE_BTN: // create and display the window for issue creation
			new IssueFrame(JiraPanel.ISSUE_FIELD_NAMES_CREATE,new HashMap());
			break;
		case PUSH_EDIT_ISSUE_BTN: // create and display the window for issue editing
			issueIndex = issuesTable.getSelectedRow();
			selectedIssueKey = issuesTable.getValueAt(issueIndex, 0);
			selectedIssue = jp.getIssueByKey((String)selectedIssueKey);
			if (selectedIssue!=null){
				new IssueFrame(JiraPanel.ISSUE_FIELD_NAMES_CREATE,selectedIssue);
			}
			else {
				lblInfo.setText("You must select an issue from the table");
			}
			break;
		case PUSH_ADD_ATTACHMENT:  // create and display a window for managing attachments
			issueIndex = issuesTable.getSelectedRow();
			selectedIssueKey = issuesTable.getValueAt(issueIndex, 0);
			selectedIssue = jp.getIssueByKey((String)selectedIssueKey);
			if (selectedIssue!=null){
				
				AttachmentChooser ac = new AttachmentChooser(selectedIssue);				

				attachmentsPopup = new JFrame("Attachment Chooser for issue "+selectedIssue.get("key"));
				
				attachmentsPopup.getContentPane().add(ac);
				attachmentsPopup.pack();
				attachmentsPopup.setVisible(true);
			}
			else {
				lblInfo.setText("You must select an issue from the table");
			}
			break;		
		case PUSH_SEE_COMMENT: // create and display a window for adding / editing comments
			issueIndex = issuesTable.getSelectedRow();
			selectedIssueKey = issuesTable.getValueAt(issueIndex, 0);
			selectedIssue = jp.getIssueByKey((String)selectedIssueKey);
			if (selectedIssue!=null){

				commentsPopup = new JFrame("Comments");
				commentsPopup.setMaximumSize(new Dimension(400,650));
				commentsPanel = createCommentsPanel((String)selectedIssue.get("key"), new JPanel());
				commentsPopup.getContentPane().add(commentsPanel);
				commentsPopup.pack();
				commentsPopup.setVisible(true);
			}
			else {
				lblInfo.setText("You must select an issue from the table");
			}
			break;		

		case PUSH_SEARCH_BTN: // search issues by user query
			jp.JiraGetIssues(tfSearchIssue.getText());
			break;
		}		
	}

	/**
	 * This method populates the window for adding/editing comments.
	 * @param issueKey - the key for the issue for which we're adding/editing comments
	 * @param rightPanel - the main panel in this window to which we'll be adding the other components
	 * @return the main panel after it's been populated with contents
	 */
	private JPanel createCommentsPanel(String issueKey, JPanel rightPanel){		
		
		rightPanel.setLayout(new BoxLayout(rightPanel,BoxLayout.PAGE_AXIS));
		JLabel l = new JLabel("Comments for issue "+issueKey+" :");
		l.setAlignmentX(JLabel.LEFT);
		rightPanel.add(l);
		
		List comments = jp.JiraGetComments(issueKey);
		
		JPanel commentsPanel = new JPanel();
		commentsPanel.setLayout(new GridLayout(0,1,5,15));			
		if (comments!=null){	// check if the selected issue already has comments to display
			Iterator it = comments.iterator();
			JPanel p;
			JTextArea c;
			JScrollPane sp;
			JPanel details;
			while (it.hasNext()) {
				HashMap h = (HashMap) it.next();
				p = new JPanel();
				p.setLayout(new BorderLayout());
				p.setBorder(BorderFactory.createEtchedBorder(EtchedBorder.LOWERED));
//				TODO: adjust the sizing of this panel to prevent it from growing out of the screen
//				p.setPreferredSize(new Dimension(990,670));
//				p.setMinimumSize(new Dimension(990,670));
				c = new JTextArea();
				c.setWrapStyleWord(true);
				c.setEditable(false);
				c.setText((String) h.get("body"));
				sp = new JScrollPane(c);
				p.add(sp,BorderLayout.CENTER);
				details = new JPanel();
				JButton btnEditComment = new JButton("Edit");
				btnEditComment.addActionListener(new AddCommentListener(h,issueKey));					
				details.add(btnEditComment);
				details.add(createDetailsPanel("Author:", (String)h.get("author"),
						"Created:", (String)h.get("created")));
				details.add(createDetailsPanel("Update author:", (String)h.get("updateAuthor"),
						"Updated:", (String)h.get("updated")));
				p.add(details,BorderLayout.SOUTH);
				commentsPanel.add(p);
			}	
		}
		else{
			commentsPanel.add(new JTextArea("This issue has no comments."));
		}
		JScrollPane commentsScrollPane = new JScrollPane(commentsPanel);
		commentsScrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
		commentsScrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);			

		rightPanel.add(commentsScrollPane);
		
		JButton btnCreateComment = new JButton(JiraPanel.PUSH_ADD_COMMENT);
		btnCreateComment.setAlignmentX(JButton.LEFT);	
		btnCreateComment.addActionListener(new AddCommentListener(issueKey));
		rightPanel.add(btnCreateComment);
		return rightPanel;			
	}
	
	/**
	 * This method fills in a panel with details on each comment
	 * @param row1Label - String for labeling the first row
	 * @param row1Value - String value for the first row contents
	 * @param row2Label - String for labeling the second row
	 * @param row2Value - String value for the second row contents
	 * @return a Panel that contains some details for a comment
	 */
	private JPanel createDetailsPanel(String row1Label, String row1Value, String row2Label, String row2Value){
		JPanel p1 = new JPanel();			
		p1.setLayout(new BoxLayout(p1,BoxLayout.Y_AXIS));
		p1.setBorder(BorderFactory.createLineBorder(TABLE_HEADER_COLOR));
		JPanel row1 = new JPanel();
		JPanel row2 = new JPanel();					
		row1.add(new JLabel(row1Label));
		JLabel l11 = new JLabel(row1Value);
		l11.setFont(JiraPanel.LABEL_ITALIC_FONT);
		row1.add(l11);
		p1.add(row1);
		row2.add(new JLabel(row2Label));
		JLabel l12 = new JLabel();
		try {
			Date date = new SimpleDateFormat(DATE_FORMAT).parse(row2Value);
			SimpleDateFormat dt1 = new SimpleDateFormat("yyyy-MM-dd");
			l12.setText(dt1.format(date));
		} catch (ParseException e) {			
			l12.setText(row2Value);
		}
		l12.setFont(JiraPanel.LABEL_ITALIC_FONT);
		row2.add(l12);
		p1.add(row2);
		p1.setAlignmentX(JPanel.LEFT_ALIGNMENT);
		return p1;
	}
	
	/**
	 * This method creates the main panel of the JiraPlugin GUI.
	 * @param jp - a JiraPlugin object reference for accessing its methods when we need to 
	 * interact with the Jira server
	 */
	public JiraPanel(JiraPlugin jp) {
		this.jp = jp;
		
		setBounds(new Rectangle(440, 10, 990, 670));
		setPreferredSize(new Dimension(990,670));
		setLayout(new CardLayout(0, 0));
		
		JPanel pPlugin = new JPanel();
		add(pPlugin, JIRA_PANEL);
		GridBagLayout gbl_pPlugin = new GridBagLayout();
		gbl_pPlugin.columnWidths = new int[]{10, 276, 61, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
		gbl_pPlugin.rowHeights = new int[]{50, 36, 50, 0, 192, 0, 0, 0, 0, 0, 0};
		gbl_pPlugin.columnWeights = new double[]{0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0};
		gbl_pPlugin.rowWeights = new double[]{0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE};
		pPlugin.setLayout(gbl_pPlugin);
		
		JPanel panel = new JPanel();
		GridBagConstraints gbc_panel = new GridBagConstraints();
		gbc_panel.fill = GridBagConstraints.HORIZONTAL;
		gbc_panel.insets = new Insets(0, 0, 5, 5);
		gbc_panel.gridwidth = 5;
		gbc_panel.anchor = GridBagConstraints.NORTH;
		gbc_panel.gridx = 1;
		gbc_panel.gridy = 0;
		pPlugin.add(panel, gbc_panel);
		panel.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
		panel.setLayout(new BorderLayout(0, 0));
		
		JLabel lblUsernameTag = new JLabel("You are logged in as :");
		lblUsernameTag.setHorizontalAlignment(SwingConstants.CENTER);
		panel.add(lblUsernameTag, BorderLayout.WEST);
		
		lblUsername = new JLabel("New label");
		lblUsername.setHorizontalAlignment(SwingConstants.CENTER);
		panel.add(lblUsername, BorderLayout.CENTER);
		
		btnChangeLogin = new JButton(CHANGE_LOGIN);
		btnChangeLogin.addActionListener(this);
		panel.add(btnChangeLogin, BorderLayout.EAST);
		
		JPanel panel_8 = new JPanel();
		GridBagConstraints gbc_panel_8 = new GridBagConstraints();
		gbc_panel_8.gridwidth = 9;
		gbc_panel_8.insets = new Insets(0, 0, 5, 5);
		gbc_panel_8.fill = GridBagConstraints.BOTH;
		gbc_panel_8.gridx = 1;
		gbc_panel_8.gridy = 8;
		pPlugin.add(panel_8, gbc_panel_8);
		panel_8.setLayout(new BoxLayout(panel_8, BoxLayout.X_AXIS));
		
		Component horizontalStrut_1 = Box.createHorizontalStrut(20);
		panel_8.add(horizontalStrut_1);
		
		JButton button_2 = new JButton(PUSH_SEARCH_BTN);
		button_2.setActionCommand(PUSH_SEARCH_BTN);
		button_2.addActionListener(this);
		panel_8.add(button_2);
		
		tfSearchIssue = new JTextField();
		tfSearchIssue.setPreferredSize(new Dimension(60, 20));
		tfSearchIssue.setColumns(50);
		panel_8.add(tfSearchIssue);
		
		JPanel panel_4 = new JPanel();
		GridBagConstraints gbc_panel_4 = new GridBagConstraints();
		gbc_panel_4.gridwidth = 7;
		gbc_panel_4.insets = new Insets(0, 0, 5, 5);
		gbc_panel_4.fill = GridBagConstraints.BOTH;
		gbc_panel_4.gridx = 1;
		gbc_panel_4.gridy = 7;
		pPlugin.add(panel_4, gbc_panel_4);
		panel_4.setLayout(new BoxLayout(panel_4, BoxLayout.X_AXIS));
		
		Component horizontalStrut = Box.createHorizontalStrut(20);
		panel_4.add(horizontalStrut);
		
		JButton button = new JButton(PUSH_CREATE_ISSUE_BTN);
		button.setActionCommand(PUSH_CREATE_ISSUE_BTN);
		button.addActionListener(this);
		button.setPreferredSize(new Dimension(200, 23));
		button.setMaximumSize(new Dimension(250, 23));
		button.setMinimumSize(new Dimension(200, 23));		
		panel_4.add(button);
		
		btnEditIssue = new JButton(PUSH_EDIT_ISSUE_BTN);
		btnEditIssue.setActionCommand(PUSH_EDIT_ISSUE_BTN);
		btnEditIssue.setEnabled(false);
		btnEditIssue.addActionListener(this);
		btnEditIssue.setPreferredSize(new Dimension(200, 23));
		btnEditIssue.setMaximumSize(new Dimension(250, 23));
		btnEditIssue.setMinimumSize(new Dimension(200, 23));
		panel_4.add(btnEditIssue);
		
		btnAddAttach = new JButton(PUSH_ADD_ATTACHMENT);
		btnAddAttach.setActionCommand(PUSH_ADD_ATTACHMENT);
		btnAddAttach.setEnabled(false);
		btnAddAttach.addActionListener(this);
		btnAddAttach.setPreferredSize(new Dimension(200, 23));
		btnAddAttach.setMinimumSize(new Dimension(250, 23));
		btnAddAttach.setMaximumSize(new Dimension(200, 23));
		panel_4.add(btnAddAttach);

		btnSeeComments = new JButton(PUSH_SEE_COMMENT);
		btnSeeComments.setActionCommand(PUSH_SEE_COMMENT);
		btnSeeComments.setEnabled(false);
		btnSeeComments.addActionListener(this);
		btnSeeComments.setPreferredSize(new Dimension(200, 23));
		btnSeeComments.setMinimumSize(new Dimension(250, 23));
		btnSeeComments.setMaximumSize(new Dimension(200, 23));
		panel_4.add(btnSeeComments);		
		
		JPanel panel_1 = new JPanel();
		panel_1.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
		GridBagConstraints gbc_panel_1 = new GridBagConstraints();
		gbc_panel_1.insets = new Insets(0, 0, 5, 5);
		gbc_panel_1.gridwidth = 5;
		gbc_panel_1.fill = GridBagConstraints.HORIZONTAL;
		gbc_panel_1.gridx = 1;
		gbc_panel_1.gridy = 1;
		pPlugin.add(panel_1, gbc_panel_1);
		panel_1.setLayout(new BorderLayout(0, 0));
		
		JLabel lblProject = new JLabel("Project:");
		panel_1.add(lblProject, BorderLayout.WEST);
		
		Component horizontalGlue_1 = Box.createHorizontalGlue();
		panel_1.add(horizontalGlue_1, BorderLayout.CENTER);
		
		cbProjects = new JComboBox(projectsDefault);
		cbProjects.setActionCommand(PROJECT_SELECTED);
		cbProjects.addActionListener(this);
		cbProjects.setPreferredSize(new Dimension(300, 30));
		cbProjects.setMinimumSize(new Dimension(160, 20));
		panel_1.add(cbProjects, BorderLayout.EAST);
		
		JPanel panel_2 = new JPanel();
		panel_2.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
		GridBagConstraints gbc_panel_2 = new GridBagConstraints();
		gbc_panel_2.insets = new Insets(0, 0, 5, 5);
		gbc_panel_2.gridwidth = 5;
		gbc_panel_2.fill = GridBagConstraints.HORIZONTAL;
		gbc_panel_2.gridx = 1;
		gbc_panel_2.gridy = 2;
		pPlugin.add(panel_2, gbc_panel_2);
		panel_2.setLayout(new BorderLayout(0, 0));
		
		JLabel lblVersion = new JLabel("Version:");
		panel_2.add(lblVersion, BorderLayout.WEST);
		
		Component horizontalGlue_2 = Box.createHorizontalGlue();
		panel_2.add(horizontalGlue_2, BorderLayout.CENTER);
		
		cbVersions = new JComboBox(versionsDefault);
		cbVersions.setActionCommand(VERSION_SELECTED);		
		cbVersions.addActionListener(this);
		cbVersions.setPreferredSize(new Dimension(300, 30));
		cbVersions.setMinimumSize(new Dimension(160, 20));
		panel_2.add(cbVersions, BorderLayout.EAST);
		
		JPanel panel_7 = new JPanel();
		panel_7.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
		GridBagConstraints gbc_panel_7 = new GridBagConstraints();
		gbc_panel_7.insets = new Insets(0, 0, 5, 5);
		gbc_panel_7.gridwidth = 5;
		gbc_panel_7.fill = GridBagConstraints.BOTH;
		gbc_panel_7.gridx = 1;
		gbc_panel_7.gridy = 3;
		pPlugin.add(panel_7, gbc_panel_7);
		panel_7.setLayout(new BorderLayout(0, 0));
		
		JLabel label = new JLabel("Component:");
		panel_7.add(label, BorderLayout.WEST);
		
		Component horizontalGlue = Box.createHorizontalGlue();
		panel_7.add(horizontalGlue, BorderLayout.CENTER);
		
		cbComponents = new JComboBox(componentsDefault);
		cbComponents.setActionCommand(COMPONENT_SELECTED);	
		cbComponents.addActionListener(this);
		cbComponents.setPreferredSize(new Dimension(300, 30));
		cbComponents.setMinimumSize(new Dimension(160, 20));
		panel_7.add(cbComponents, BorderLayout.EAST);
		
		JPanel panel_3 = new JPanel();
		GridBagConstraints gbc_panel_3 = new GridBagConstraints();
		gbc_panel_3.gridheight = 3;
		gbc_panel_3.insets = new Insets(0, 0, 5, 5);
		gbc_panel_3.gridwidth = 12;
		gbc_panel_3.fill = GridBagConstraints.BOTH;
		gbc_panel_3.gridx = 1;
		gbc_panel_3.gridy = 4;
		pPlugin.add(panel_3, gbc_panel_3);
		panel_3.setLayout(new BoxLayout(panel_3, BoxLayout.Y_AXIS));
		
		JLabel label_1 = new JLabel("Issues for project ...");
		panel_3.add(label_1);
		
		scrollPane = new JScrollPane(this.issuesTable,JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);		
		panel_3.add(scrollPane);
		
		lblInfo = new JLabel("Info");
		GridBagConstraints gbc_lblInfo = new GridBagConstraints();
		gbc_lblInfo.fill = GridBagConstraints.HORIZONTAL;
		gbc_lblInfo.insets = new Insets(0, 0, 0, 5);
		gbc_lblInfo.gridx = 1;
		gbc_lblInfo.gridy = 9;
		pPlugin.add(lblInfo, gbc_lblInfo);
		
		JPanel pLogin = new JPanel();
		add(pLogin, LOGIN_PANEL);
		pLogin.setLayout(new BorderLayout(0, 0));
		
		JPanel panel_5 = new JPanel();
		panel_5.setPreferredSize(new Dimension(310, 300));
		pLogin.add(panel_5, BorderLayout.CENTER);
		GridBagLayout gbl_panel_5 = new GridBagLayout();
		gbl_panel_5.columnWidths = new int[] {10, 84, 350, 30, 0};
		gbl_panel_5.rowHeights = new int[]{77, 99, 65, 62, 62, 0, 0};
		gbl_panel_5.columnWeights = new double[]{0.0, 0.0, 1.0, 1.0, Double.MIN_VALUE};
		gbl_panel_5.rowWeights = new double[]{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE};
		panel_5.setLayout(gbl_panel_5);
		
		Component verticalGlue = Box.createVerticalGlue();
		verticalGlue.setPreferredSize(new Dimension(0, 60));
		GridBagConstraints gbc_verticalGlue = new GridBagConstraints();
		gbc_verticalGlue.fill = GridBagConstraints.VERTICAL;
		gbc_verticalGlue.insets = new Insets(0, 0, 5, 5);
		gbc_verticalGlue.gridx = 1;
		gbc_verticalGlue.gridy = 0;
		panel_5.add(verticalGlue, gbc_verticalGlue);
		
		Component horizontalGlue_3 = Box.createHorizontalGlue();
		horizontalGlue_3.setPreferredSize(new Dimension(140, 0));
		horizontalGlue_3.setMinimumSize(new Dimension(40, 0));
		GridBagConstraints gbc_horizontalGlue_3 = new GridBagConstraints();
		gbc_horizontalGlue_3.fill = GridBagConstraints.VERTICAL;
		gbc_horizontalGlue_3.insets = new Insets(0, 0, 5, 5);
		gbc_horizontalGlue_3.gridx = 0;
		gbc_horizontalGlue_3.gridy = 1;
		panel_5.add(horizontalGlue_3, gbc_horizontalGlue_3);
		
		JLabel lblNewLabel = new JLabel("Please fill in your Jira login information below:");
		lblNewLabel.setFont(JiraPanel.LABEL_FONT);
		lblNewLabel.setVerticalAlignment(SwingConstants.BOTTOM);
		GridBagConstraints gbc_lblNewLabel = new GridBagConstraints();
		gbc_lblNewLabel.fill = GridBagConstraints.VERTICAL;
		gbc_lblNewLabel.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel.gridx = 2;
		gbc_lblNewLabel.gridy = 1;
		panel_5.add(lblNewLabel, gbc_lblNewLabel);
		
		Component horizontalGlue_4 = Box.createHorizontalGlue();
		horizontalGlue_4.setPreferredSize(new Dimension(140, 0));
		horizontalGlue_4.setMinimumSize(new Dimension(40, 0));
		GridBagConstraints gbc_horizontalGlue_4 = new GridBagConstraints();
		gbc_horizontalGlue_4.fill = GridBagConstraints.HORIZONTAL;
		gbc_horizontalGlue_4.insets = new Insets(0, 0, 5, 0);
		gbc_horizontalGlue_4.gridx = 3;
		gbc_horizontalGlue_4.gridy = 1;
		panel_5.add(horizontalGlue_4, gbc_horizontalGlue_4);
		
		JLabel lblNewLabel_2 = new JLabel("Username :");
		GridBagConstraints gbc_lblNewLabel_2 = new GridBagConstraints();
		gbc_lblNewLabel_2.anchor = GridBagConstraints.EAST;
		gbc_lblNewLabel_2.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel_2.gridx = 1;
		gbc_lblNewLabel_2.gridy = 2;
		panel_5.add(lblNewLabel_2, gbc_lblNewLabel_2);
		
		tfUsername = new JTextField();
		GridBagConstraints gbc_tfUsername = new GridBagConstraints();
		gbc_tfUsername.fill = GridBagConstraints.HORIZONTAL;
		gbc_tfUsername.insets = new Insets(0, 0, 5, 5);
		gbc_tfUsername.gridx = 2;
		gbc_tfUsername.gridy = 2;
		panel_5.add(tfUsername, gbc_tfUsername);
		tfUsername.setColumns(10);
		
		JLabel lblNewLabel_1 = new JLabel("Password :");
		GridBagConstraints gbc_lblNewLabel_1 = new GridBagConstraints();
		gbc_lblNewLabel_1.anchor = GridBagConstraints.EAST;
		gbc_lblNewLabel_1.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel_1.gridx = 1;
		gbc_lblNewLabel_1.gridy = 3;
		panel_5.add(lblNewLabel_1, gbc_lblNewLabel_1);
		
		btnLogin = new JButton(LOGIN);
		btnLogin.addActionListener(this);
		btnLogin.setMinimumSize(new Dimension(157, 23));
		btnLogin.setMaximumSize(new Dimension(200, 23));
		btnLogin.setPreferredSize(new Dimension(157, 23));
	
		tfPassword = new JPasswordField();
		GridBagConstraints gbc_tfPassword = new GridBagConstraints();
		gbc_tfPassword.insets = new Insets(0, 0, 5, 5);
		gbc_tfPassword.fill = GridBagConstraints.HORIZONTAL;
		gbc_tfPassword.gridx = 2;
		gbc_tfPassword.gridy = 3;
		panel_5.add(tfPassword, gbc_tfPassword);
		
		JLabel lblJiraServer = new JLabel("Jira server :");
		GridBagConstraints gbc_lblJiraServer = new GridBagConstraints();
		gbc_lblJiraServer.anchor = GridBagConstraints.EAST;
		gbc_lblJiraServer.insets = new Insets(0, 0, 5, 5);
		gbc_lblJiraServer.gridx = 1;
		gbc_lblJiraServer.gridy = 4;
		panel_5.add(lblJiraServer, gbc_lblJiraServer);
		
		tfJiraServer = new JTextField();
		tfJiraServer.setColumns(10);
		tfJiraServer.setText(jp.DEFAULT_JIRA_SERVER);
		GridBagConstraints gbc_tfJiraServer = new GridBagConstraints();
		gbc_tfJiraServer.insets = new Insets(0, 0, 5, 5);
		gbc_tfJiraServer.fill = GridBagConstraints.HORIZONTAL;
		gbc_tfJiraServer.gridx = 2;
		gbc_tfJiraServer.gridy = 4;
		panel_5.add(tfJiraServer, gbc_tfJiraServer);
		GridBagConstraints gbc_btnLogin = new GridBagConstraints();
		gbc_btnLogin.insets = new Insets(0, 0, 0, 5);
		gbc_btnLogin.gridx = 2;
		gbc_btnLogin.gridy = 5;
		panel_5.add(btnLogin, gbc_btnLogin);		
		
		showPanel(LOGIN_PANEL);

	}
	
	/**
	 * The MyTable class extends the JTable class to be able to use a different Table renderer.
	 */
	class MyTable extends JTable{
		public MyTable(MyTableModel myTableModel) {
			// TODO Auto-generated constructor stub
			super(myTableModel);
			setRowHeight(35);
			Enumeration<TableColumn> e = this.getColumnModel().getColumns();
			while (e.hasMoreElements()){
				 TableColumn c = e.nextElement();
				 c.setCellRenderer(new TableCellLongTextRenderer());
			}
		}
	}
	/**
	 * The MyTableModel class extends the DefaultTableModel class to be able to set editing permissions 
	 * on table cells.
	 */
	class MyTableModel extends DefaultTableModel {
		
		public MyTableModel(Object[][] tableData, Object[] columnNames){
			super(tableData,columnNames);						
		}
	    public boolean isCellEditable(int row, int col){    		    	
	    	return false;
	    }
		
	}
	
	/** 
	 * This class defines a table renderer to properly wrap long text in the table 
	 * @author Paul Zepernick 
	 */  
	class TableCellLongTextRenderer extends DefaultTableCellRenderer implements TableCellRenderer{  
	  
	    @Override  
	    public Component getTableCellRendererComponent(JTable table, Object value, boolean isSelected, boolean hasFocus, int row, int column) {  
	        final JTextArea jtext = new JTextArea();  
	        jtext.setText((String)value);  
	        jtext.setWrapStyleWord(true);  
	        jtext.setLineWrap(true);
	        jtext.setToolTipText((String)value);        
	        
			if (row%2==1) {
				 jtext.setBackground(JiraPanel.TABLE_ODD_ROW_COLOR);
				 }
			else{
				 jtext.setBackground(Color.WHITE);
				 }
	        if(isSelected){  
	            jtext.setBackground((Color)UIManager.get("Table.selectionBackground"));  
	        }  
	        return jtext;  
	    }  
	  
	    //METHODS overridden for performance  
	    @Override  
	    public void validate() {  
	    }  
	  
	    @Override  
	    public void revalidate() {  
	    }  
	  
	    @Override  
	    public void firePropertyChange(String propertyName, Object oldValue, Object newValue) {  
	    }  
	  
	     public void firePropertyChange(String propertyName, boolean oldValue, boolean newValue) {}  
	  
	} 	
	
	
	/** 
	 * The IssueFrame class defines a window for creating / editing an issue.
	 */ 
	class IssueFrame extends JFrame implements ActionListener {
		JComboBox cbProject;
		JComboBox cbType;
		JComboBox cbPriority;
		JComboBox cbStatus;
		JDateChooser dateChooser;
		MultiCombo mcbFixVersions;
		MultiCombo mcbAffectsVersions;
		MultiCombo mcbComponents;
		JTextArea taDescription;
		JTextArea taEnvironment;
		AttachmentChooser ac;
		JTextField tfReporter;
		JTextField tfSummary;				
		JPanel contentsPanel;
		JPanel buttonsPanel;
		HashMap<String,JComponent> panelComponents = new HashMap();
		HashMap issue;
		
		/** 
		 * The IssueFrame constructor
		 * @param fieldNames - array of Strings that identify the fields of an issue 
		 * which will appear in the window to be edited
		 * @param issue - HashMap object containing issue data (can be a new empty HashMap in the case of issue creation)
		 */
		public IssueFrame(String[] fieldNames, HashMap issue){
			super();
			
			this.issue = issue;			
			
			this.setAlwaysOnTop(true);
			this.setLocation(200,100);			
			
			JButton btnSave = new JButton("Save");
			btnSave.addActionListener(this);
			JButton btnCancel = new JButton("Cancel");
			btnCancel.addActionListener(this);
			
			buttonsPanel = new JPanel();
			buttonsPanel.setBorder(BorderFactory.createEtchedBorder(EtchedBorder.LOWERED));
			buttonsPanel.add(btnSave);
			buttonsPanel.add(btnCancel);
			
			add(createObjects(fieldNames,jp.getProjects(),jp.getIssueTypes(),jp.getPriorities(),jp.getStatuses()),BorderLayout.CENTER);
			add(buttonsPanel,BorderLayout.SOUTH);

			this.pack();
			this.setVisible(true);
		}
		
		/** 
		 * The createObjects method creates the components in the window used for creating/editing an issue 
		 * @param fieldNames - array of Strings that identify the fields the issue 
		 * which will appear in the window to be edited
		 * @param projects - array of HashMap objects representing the available projects
		 * @param types - array of HashMap objects that represent the possible issue types
		 * @param priorities - array of HashMap objects that represent the possible priorities
		 * @param statuses - array of HashMap objects that represent the possible statuses
		 * @return a JPanel object containing all the components that store the issue data
		 */
		private JPanel createObjects(String[] fieldNames,Object[] projects, Object[] types, Object[] priorities, Object[] statuses) {
			contentsPanel = new JPanel();
			contentsPanel.setBorder(BorderFactory.createEtchedBorder(EtchedBorder.LOWERED));
			contentsPanel.setLayout(new BoxLayout(contentsPanel, BoxLayout.PAGE_AXIS));
			JPanel[] panels = new JPanel[fieldNames.length];
			JLabel[] labels = new JLabel[fieldNames.length];			
			for (int i=0; i<fieldNames.length; i++){
				panels[i] = new JPanel();
				panels[i].setBorder(BorderFactory.createEtchedBorder(EtchedBorder.LOWERED));
				panels[i].setLayout(new FlowLayout(FlowLayout.LEFT,20,10));
				labels[i] = new JLabel(fieldNames[i]);
				labels[i].setFont(JiraPanel.LABEL_FONT);
				labels[i].setPreferredSize(new Dimension(120,25));
				labels[i].setHorizontalAlignment(JLabel.RIGHT);
				labels[i].setVerticalAlignment(JLabel.TOP);
				labels[i].setAlignmentX(JLabel.LEFT_ALIGNMENT);
				panels[i].add(labels[i]);
				contentsPanel.add(panels[i]);				
				panelComponents.put(fieldNames[i],panels[i]);
				
			}
			// Project ComboBox
			cbProject = new JComboBox();					
			cbProject.setEditable(true);
			cbProject.setPreferredSize(new Dimension(150,25));
			cbProject.setActionCommand(PROJECT_SELECTED);
			cbProject.addActionListener(this);
			setComboValues(cbProject, jp.getProperty(projects,"name"));
			new JiraS16MaximumMatch(cbProject);
			panelComponents.get("project").add(cbProject);
			// END Project ComboBox
			// Type ComboBox
			cbType = new JComboBox();					
			cbType.setEditable(true);
			cbType.setPreferredSize(new Dimension(150,25));
			setComboValues(cbType, jp.getProperty(types,"name"));
			new JiraS16MaximumMatch(cbType);
			panelComponents.get("type").add(cbType);
			// END Type ComboBox
			// Priority ComboBox
			cbPriority = new JComboBox();					
			cbPriority.setEditable(true);
			cbPriority.setPreferredSize(new Dimension(150,25));
			setComboValues(cbPriority, jp.getProperty(priorities,"name"));
			new JiraS16MaximumMatch(cbPriority);
			panelComponents.get("priority").add(cbPriority);
			// END Priority ComboBox	
			// Status ComboBox
			cbStatus = new JComboBox();					
			cbStatus.setEditable(true);
			cbStatus.setPreferredSize(new Dimension(150,25));
			setComboValues(cbStatus, jp.getProperty(statuses,"name"));
			new JiraS16MaximumMatch(cbStatus);
			panelComponents.get("status").add(cbStatus);
			// END Status ComboBox
			// fixVersions Combo
			mcbFixVersions = new MultiCombo();				
//			mcbFixVersions.list.getDocument().addDocumentListener(new MyDocumentListener("fixVersions"));
			panelComponents.get("fixVersions").add(mcbFixVersions);
			// END fixVersions Combo				
			// affectsVersions Combo
			mcbAffectsVersions = new MultiCombo();
//			mcbAffectsVersions.list.getDocument().addDocumentListener(new MyDocumentListener("affectsVersions"));
			panelComponents.get("affectsVersions").add(mcbAffectsVersions);
			// END affectsVersions Combo
			// components Combo
			mcbComponents = new MultiCombo();
//			mcbComponents.list.getDocument().addDocumentListener(new MyDocumentListener("components"));
			panelComponents.get("components").add(mcbComponents);
			// END components Combo
			// duedate DateChooser		
			dateChooser = new JDateChooser();					
			dateChooser.setDateFormatString(DATE_FORMAT);
			dateChooser.setPreferredSize(new Dimension(200,25));
//			dateChooser.actionPerformed(arg0)
			panelComponents.get("duedate").add(dateChooser);
			// END duedate DateChooser
			// description TextArea
			taDescription = new JTextArea(2,20);		
			taDescription.setLineWrap(true);
			taDescription.setWrapStyleWord(true);	
//			taDescription.getDocument().addDocumentListener(new MyDocumentListener("description"));
			JScrollPane js = new JScrollPane(taDescription);
			js.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
			js.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);			
			panelComponents.get("description").add(taDescription);
			// END description TextArea
			// environment TextArea
			taEnvironment = new JTextArea(2,20);		
			taEnvironment.setLineWrap(true);
			taEnvironment.setWrapStyleWord(true);
//			taEnvironment.getDocument().addDocumentListener(new MyDocumentListener("environment"));
			js = new JScrollPane(taEnvironment);
			js.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
			js.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);			
			panelComponents.get("environment").add(taEnvironment);
			// END environment TextArea			
			// AttachmentChooser
			ac = new AttachmentChooser(issue);
			panelComponents.get("attachmentNames").add(ac);
			// END AttachmentChooser
			// reporter TextField			
			tfReporter = new JTextField();
			tfReporter.setPreferredSize(new Dimension(200,25));
			panelComponents.get("reporter").add(tfReporter);
			// END reporter TextField
			// summary TextField			
			tfSummary = new JTextField();
			tfSummary.setPreferredSize(new Dimension(200,25));
//			tfSummary.getDocument().addDocumentListener(new MyDocumentListener("summary"));
			panelComponents.get("summary").add(tfSummary);
			// END reporter TextField			
			if (issue.containsKey("key")){  // this issue is being edited
				this.setTitle("Editing issue "+issue.get("key"));
				// set project
				String projectName = jp.getFieldValue(issue, "project");
//				System.out.print(projectName);
				cbProject.setSelectedItem(projectName);
				// set type
				String typeName = jp.getFieldValue(issue, "type");
//				System.out.print(typeName);
				cbType.setSelectedItem(typeName);
				// set priority
				String priorityName = jp.getFieldValue(issue, "priority");
//				System.out.print(priorityName);
				cbPriority.setSelectedItem(priorityName);
				// set status
				String statusName = jp.getFieldValue(issue, "status");
				Object[] acts = jp.JiraGetAvailableActions((String) issue.get("key"));
				setComboValues(cbStatus, jp.getProperty(acts,"name"));
//				System.out.print(statusName);
//				cbStatus.setSelectedItem(statusName);
				// set fixVersions
				mcbFixVersions.list.setText(jp.getFieldValue(issue, JiraPlugin.FIX_VERSIONS_FIELD));
				// set components
				mcbComponents.list.setText(jp.getFieldValue(issue, JiraPlugin.COMPONENTS_FIELD));
				// set affectsVersions
				mcbAffectsVersions.list.setText(jp.getFieldValue(issue, JiraPlugin.AFFECTS_VERSIONS_FIELD));
				// set duedate
				try {
					if (!issue.get("duedate").toString().equals("None")){
						Date date = new SimpleDateFormat(DATE_FORMAT).parse(issue.get("duedate").toString());
						dateChooser.setDate(date);	
					}					
				} catch (ParseException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}	
				// set description
				taDescription.setText(jp.getFieldValue(issue,"description"));
				// set environment
				taEnvironment.setText(jp.getFieldValue(issue,"environment"));				
				// set reporter
				tfReporter.setText(jp.getFieldValue(issue, "reporter"));
				// set summary
				tfSummary.setText(jp.getFieldValue(issue, "summary"));
			}		
			else{
				this.setTitle("Create new issue ");
				cbStatus.setSelectedItem("Open");
				cbStatus.setEnabled(false);			
			}
			tfReporter.setText(lblUsername.getText());
			tfReporter.setEditable(false);
			return contentsPanel;
		}

		/**
		 * This method treats the user events that occur in the IssuePanel.
		 * @param arg0 - the user event
		 */
		@Override
		public void actionPerformed(ActionEvent arg0) {
			lblInfo.setText("Info");
			switch (arg0.getActionCommand()){
			case "Cancel":
				this.dispose();				
				break;
			case "Save":		
				issue.put(jp.PROJECT_FIELD, jp.getIdFromName(jp.PROJECT_FIELD, (String) cbProject.getSelectedItem()));
				issue.put(jp.TYPE_FIELD, jp.getIdFromName(jp.TYPE_FIELD, (String) cbType.getSelectedItem()));
				issue.put(jp.PRIORITY_FIELD, jp.getIdFromName(jp.PRIORITY_FIELD, (String) cbPriority.getSelectedItem()));
				if (cbStatus.isEnabled()){
					issue.put(jp.STATUS_FIELD, jp.getIdFromName(jp.getActions(),(String)cbStatus.getSelectedItem()));	
				}
				else{
					issue.put(jp.STATUS_FIELD, jp.getIdFromName(jp.STATUS_FIELD,(String)cbStatus.getSelectedItem()));
				}				
				issue.put("summary", tfSummary.getText());
				issue.put("description", taDescription.getText());
				issue.put("environment", taEnvironment.getText());
				issue.put("reporter", tfReporter.getText());				
				if (dateChooser.getDate()!=null){						
					Date date = dateChooser.getDate();
					String fDate = new SimpleDateFormat(DATE_FORMAT).format(date);
					issue.put("duedate",fDate);						
				}			
				String fixVersions = mcbFixVersions.list.getText();
				String[] names = fixVersions.split("; ");
				issue.put("fixVersions", jp.getObjects("versions", names));
				String affectsVersions = mcbAffectsVersions.list.getText();
				names = affectsVersions.split("; ");
				issue.put("affectsVersions", jp.getObjects("versions", names));
				String comps = mcbComponents.list.getText();
				names = comps.split("; ");
				issue.put("components", jp.getObjects("components", names));
				if (issue.containsKey("key")){ // this is edit issue
					jp.JiraUpdateIssue(issue);					
				}else{ // this is create issue
					jp.JiraCreateIssue(issue);
				}
				this.dispose();
				break;
			case PROJECT_SELECTED:
				
				Object[] versions = jp.JiraGetVersions(cbProject.getSelectedIndex());
				
				if (versions!=null){
					String[] verList = jp.getProperty(versions, "name");
					setComboValues(mcbFixVersions.cb, verList);				
					setComboValues(mcbAffectsVersions.cb, verList);
					mcbFixVersions.cb.setEnabled(true);
					mcbAffectsVersions.cb.setEnabled(true);				
				}
				else {
					mcbFixVersions.cb.setEnabled(false);
					mcbAffectsVersions.cb.setEnabled(false);
				}
				
				Object[] components = jp.JiraGetComponents(cbProject.getSelectedIndex());				
				if (components!=null){
					setComboValues(mcbComponents.cb, jp.getProperty(components, "name"));
					mcbComponents.cb.setEnabled(true);
				}
				else{
					mcbComponents.cb.setEnabled(false);
				}				
				break;				
			}
		}
		
		/**
		 * The class MultiCombo defines a panel that contains a JComboBox, JButton and JTextField 
		 * used to allow the user to make multiple selections from the ComboBox  
		 */
	    private class MultiCombo extends JPanel implements ActionListener {
	    	
	        JComboBox cb = new JComboBox();
	        JButton addToList = new JButton("Add");
	        JTextField list = new JTextField();
	        
	        public MultiCombo(){
	        	addToList.addActionListener(this);
	        	cb.setPreferredSize(new Dimension(150,20));
	        	list.setPreferredSize(new Dimension(200,20));
				setLayout(new BorderLayout());
				add(cb,BorderLayout.CENTER);
				add(addToList,BorderLayout.LINE_END);
				add(list,BorderLayout.PAGE_END);
	        }

			@Override
			public void actionPerformed(ActionEvent arg0) {
				String text = list.getText();
				if (text.equals("")){
					list.setText((String) cb.getSelectedItem());
				}
				else{
					list.setText(text+"; "+cb.getSelectedItem());
				}
			}
	    }	    
	}
	
	/**
	 * The class AttachmentChooser defines a panel that contains components 
	 * used to allow the user to manipulate attachments for an issue  
	 */
	class AttachmentChooser extends JPanel implements ActionListener {
		HashMap i;
		List attachmentList = new LinkedList();
		DefaultListModel model = new DefaultListModel();
		JList att;		
		JButton addAttach; 
        JButton remAttach;
        JButton getAttach;
        File file;
        final JFileChooser fc = new JFileChooser();
        final Font FILENAME_LABEL_FONT = new Font("Tahoma",Font.ITALIC,12); 
        /**
		 * Constructor 
		 * @param issue - HashMap object that contains issue data   
		 */
        public AttachmentChooser(HashMap issue){
        	this();
        	this.i=issue;
        	if (i.containsKey("key")){ // this is not an issue waiting to be created
        		this.setContents();
        	}
        	else{
        		getAttach.setEnabled(false); // at issue creation this option is unavailable        		
        	}
        }
		/**
		 * Constructor - creates components in the window that displays attachments   
		 */
        public AttachmentChooser(){
        	// TODO Fix problem about size of the JList
        	att = new JList(model);
            att.setMinimumSize(new Dimension(100,150));
        	att.setPreferredSize(new Dimension(100,150));
        	att.setMaximumSize(new Dimension(100,150));
        	att.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);       	
        	att.setVisibleRowCount(4);        	
        	att.setFont(FILENAME_LABEL_FONT);
        	JScrollPane js = new JScrollPane(att);
        	js.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        	add(js);        	
        	JPanel buttonsPanel = new JPanel();
        	buttonsPanel.setLayout(new BoxLayout(buttonsPanel,BoxLayout.Y_AXIS));
        	addAttach = new JButton("Add file");
        	addAttach.addActionListener(this);        
        	addAttach.setMinimumSize(new Dimension(120,20));     
        	addAttach.setEnabled(true);
            buttonsPanel.add(addAttach);
            remAttach = new JButton("Remove file");
            remAttach.addActionListener(this);            
            remAttach.setMinimumSize(new Dimension(120,20));
            remAttach.setEnabled(true);
            buttonsPanel.add(remAttach);
            getAttach = new JButton("Download file");
            getAttach.addActionListener(this);            
            getAttach.setMinimumSize(new Dimension(120,20));
            getAttach.setEnabled(true);
            buttonsPanel.add(getAttach);
            add(buttonsPanel);            
        }  
        
		/**
		 * This method is called when the attachments window is created to fill 
		 * in its contents if the issue already has attachments  
		 */
        public void setContents(){
        	model.clear();
	    	if (i.containsKey("attachments")){
	    		Object[] atts = (Object[]) i.get("attachments");
	    		attachmentList = new LinkedList(Arrays.asList(atts));
	    		String[] attNames = jp.getProperty(atts, "filename");
	    		for (String name: attNames){
	    			model.add(0,name);
	    		}
	    	}
        }
        /**
		 * This method treats user events in the window   
		 */    
		@Override
		public void actionPerformed(ActionEvent arg0) {
			if (arg0.getSource() == addAttach) {
				int returnVal = fc.showOpenDialog(AttachmentChooser.this);
				if (returnVal == JFileChooser.APPROVE_OPTION) {
					file = fc.getSelectedFile();				
					int pos = att.getModel().getSize();
					model.add(pos, file.getName());	
					HashMap newFile = new HashMap();
					newFile.put("filename",file.getName());
					newFile.put("path", file.getAbsolutePath());
					System.out.println("Should upload "+newFile.get("filename"));
					HashMap newAttach = jp.uploadAttach(newFile);					
					if (newAttach!=null){
						attachmentList.add(newAttach);						
					}
					// add attachment in Jira
					if (i.containsKey("key")){ // only if this issue is being edited, because we need the issue key
						Object[] attachments = {newAttach};					
						jp.JiraAddAttachment((String)i.get("key"), attachments);
					}
				}
			}
			if (arg0.getSource() == remAttach) {	
				int index = att.getSelectedIndex();
				if (index>=0) {					
					HashMap selectedAttachment = getAttachmentByName((String) att.getSelectedValue());
					if (selectedAttachment!=null){
//						TODO: add backend code to support attachment delete
						System.out.println("TODO: Should delete "+selectedAttachment.get("filename"));
					}
					model.remove(att.getSelectedIndex());
				}
			}
			if (arg0.getSource() == getAttach) {	
				int index = att.getSelectedIndex();
				if (index>=0) {
					HashMap selectedAttachment = getAttachmentByName((String) att.getSelectedValue());
					if (selectedAttachment!=null){
//						TODO: add backend code to support attachment download
						System.out.println("TODO: Should download "+selectedAttachment.get("filename"));
					}
				}
			}
			if (attachmentList.size()>0){
				i.put("attachments", attachmentList.toArray());
				i.put(JiraPanel.ISSUE_FIELD_ATTACHMENT, jp.getProperty(attachmentList.toArray(), "filename"));
			}
		}
		/**
		 * This method returns an attachment (HashMap object) from the list, given its filename
		 * @param filename - the filename selected by the user in the list (String)
		 * @return attachment object (HashMap)   
		 */
		public HashMap getAttachmentByName(String filename){
			Iterator it = attachmentList.iterator();
			while (it.hasNext()){
				HashMap h = (HashMap) it.next();
				if (h.get("filename").equals(filename)){
					return h;
				}
			}
			return null;
		}
    }
	
	/**
	 * The class AddCommentListener treats user actions related to 
	 * creating/editing comments   
	 */
	class AddCommentListener implements ActionListener {
		HashMap comment;
		String issueKey;
		JFrame attPopup;
		/**
		 * Constructor
		 * @param issueKey - the key of the issue to add/edit comments   
		 */		
		public AddCommentListener(String issueKey){			
			this.issueKey = issueKey;			
		}
		/**
		 * Constructor
		 * @param issueKey - the key of the issue to add/edit comments
		 * @param comment - a HashMap comment object that is an existing comment of the issue   
		 */		
		public AddCommentListener(HashMap comment,String issueKey){
			this(issueKey);
			this.comment = comment;
//			System.out.println(comment.get("body"));
		}

		/**
		 * Method that treats user events   
		 */		
		@Override
		public void actionPerformed(ActionEvent arg0) {
			AddCommentPanel ac;
			if (comment!=null){ // create a pop-up window to edit the comment
				attPopup = new JFrame("Edit Comment");
				ac = new AddCommentPanel(comment, issueKey,attPopup);
			}
			else{ // create a pop-up window to input a new comment
				attPopup = new JFrame("New Comment");
				ac = new AddCommentPanel(issueKey,attPopup);
			}				
			attPopup.setBounds(100,200,400,350);
			attPopup.pack();
			attPopup.setVisible(true);					
		}
		
	}
	/**
	 * The class AddCommentPanel creates the pop-up window
	 * where the user creates/edits comments and treats user events on this window
	 */
	class AddCommentPanel extends JPanel implements ActionListener {
		HashMap newComment;
		String issueKey;
		JTextArea comment;		
		JButton addComment; 
		JScrollPane js;
        JButton cancel;
        JFrame frame;
    	/**
    	 * Constructor
    	 * @param oldComment - HashMap comment object of an old comment being edited
    	 * @param issueKey - the key of the issue to which the comment belongs (String)
    	 * @param parent - 
    	 */     
        public AddCommentPanel(HashMap oldComment, String issueKey, JFrame parent){
        	this(issueKey, parent);
        	newComment = oldComment;
//        	System.out.println(oldComment.get("body"));
        	comment.setText((String) oldComment.get("body"));
        	js.setViewportView(comment);
        }
        public AddCommentPanel(String issueKey, JFrame parent){
        	this(parent);
        	this.issueKey=issueKey;        	
        	comment.setText("");
        	comment.setMinimumSize(new Dimension(200,50));
        	js.setViewportView(comment);
        }
        public AddCommentPanel(JFrame parent){
        	// TODO Fix problem about size of the JList
        	frame = parent;        	
        	frame.getContentPane().add(this);
        	
        	newComment = new HashMap();
        	
        	comment = new JTextArea(10,20);
        	comment.setWrapStyleWord(true);
        	comment.setMinimumSize(new Dimension(200,50));
        	js = new JScrollPane(comment);
        	js.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        	js.setMinimumSize(new Dimension(200,50));
        	add(js);        	
        	JPanel buttonsPanel = new JPanel();
        	buttonsPanel.setLayout(new BoxLayout(buttonsPanel,BoxLayout.Y_AXIS));
        	addComment = new JButton("Save");
        	addComment.setAlignmentX(JButton.LEFT_ALIGNMENT);
        	addComment.addActionListener(this);        
        	addComment.setMinimumSize(new Dimension(120,20));        	
            buttonsPanel.add(addComment);
            cancel = new JButton("Cancel");
            cancel.addActionListener(this);            
            cancel.setMinimumSize(new Dimension(120,20));
            buttonsPanel.add(cancel);            
            add(buttonsPanel);
        }     
	        
		@Override
		public void actionPerformed(ActionEvent arg0) {
			// TODO Auto-generated method stub
			if (arg0.getSource() == addComment) {
				newComment.put("body", comment.getText());
				newComment.put("updateAuthor", lblUsername.getText());
				Date now = new Date();
				newComment.put("updated", new SimpleDateFormat(DATE_FORMAT).format(now));
				if (!newComment.containsKey("author")){
					newComment.put("author", lblUsername.getText());					
				}
				if (!newComment.containsKey("created")){
					newComment.put("created", new SimpleDateFormat(DATE_FORMAT).format(now));
				}
				jp.JiraUpdateComment(newComment,issueKey);
				commentsPopup.remove(commentsPanel);
				commentsPanel = createCommentsPanel(issueKey,new JPanel());
				commentsPopup.setContentPane(commentsPanel);
				Dimension rightSize = commentsPanel.getPreferredSize();				
				commentsPopup.setSize((int)rightSize.getWidth(),(int)rightSize.getHeight()+100);
				commentsPopup.revalidate();

			}
			frame.dispose();
		}
    }
	    
}
