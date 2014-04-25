/*
File: JiraPlugin.java ; This file is part of Twister.
Version: 2.004

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
import java.awt.Component;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Properties;

import javax.swing.JFrame;

import javax.swing.JOptionPane;
import javax.xml.bind.DatatypeConverter;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Result;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import com.twister.CustomDialog;
import com.twister.Item;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;
import org.w3c.dom.Node;


public class JiraPlugin extends BasePlugin implements TwisterPluginInterface {
	/**
	 * The JiraPlugin class implements methods to interact with the Jira server via the CE.
	 * It initializes the GUI of the JiraPlugin. 
	 */	
	
//	for debugging as standalone app
	private JFrame mainWindow;
	private static boolean isApplet = true;
//	for debugging as standalone app	
	
	final static String DEFAULT_JIRA_SERVER = "http://localhost:8080";
	
	final static String PROJECT_FIELD = "project";
	final static String STATUS_FIELD = "status";
	final static String TYPE_FIELD = "type";
	final static String PRIORITY_FIELD = "priority";
	final static String RESOLUTION_FIELD = "resolution";
	final static String VERSIONS_FIELD = "versions";
	final static String FIX_VERSIONS_FIELD = "fixVersions";
	final static String AFFECTS_VERSIONS_FIELD = "affectsVersions";
	final static String COMPONENTS_FIELD = "components";
	final static String[] ID_FIELDS = {PROJECT_FIELD, STATUS_FIELD, TYPE_FIELD, PRIORITY_FIELD, RESOLUTION_FIELD, FIX_VERSIONS_FIELD, AFFECTS_VERSIONS_FIELD, COMPONENTS_FIELD};
	final static String[] ISSUE_FIELD_NAMES = {"key","project", "type", "priority", "summary","description", 
        "environment", "status", "resolution","components","affectsVersions","fixVersions","attachmentNames","reporter","assignee",
        "created", "duedate"};
	
	
	private static Hashtable<String, String> variables;
	private Hashtable jiraElements = new Hashtable();
	private Object[] projects;
	private Object[] jiraVersions;
	private Object[] jiraComponents;
	private Object[] issueTypes;
	private Object[] priorities;
	private Object[] statuses;	
	private Object[] actions;
	private List issues;
	private HashMap comments = new HashMap();
	
	private String jiraserver;
	
	JiraPanel p;	
	
	private XmlRpcClient client;
	
	@Override
	public void init(ArrayList <Item>suite,ArrayList <Item>suitetest,
			  final Hashtable<String, String>variables,
			  Document pluginsConfig,Applet container){
		super.init(suite, suitetest, variables,pluginsConfig,container);

		System.out.println("Initializing "+getName()+" ...");
		
		this.variables = variables;

		initializeRPC();
		
		p = new JiraPanel(this);
		
        if (isApplet){
        	//createXMLStructure();
        	//uploadPluginsFile();
            Node jiraServerNode = getPropValue("jiraserver");
            jiraserver = jiraServerNode.getTextContent();
        }
        else{            
        	mainWindow = new JFrame("Jira Plugin");
    		mainWindow.add(p);
    		mainWindow.pack();
    		mainWindow.setVisible(true);
    		mainWindow.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);        	
        }
        
		System.out.println(getName()+" initialized");
	}
	
//	/*
//     * method to copy plugins configuration file
//     * to server 
//     */
//    public boolean uploadPluginsFile(){
//        try{
//            DOMSource source = new DOMSource(pluginsConfig);
//            File file = new File(variables.get("pluginslocalgeneralconf"));
//            Result result = new StreamResult(file);
//            TransformerFactory transformerFactory = TransformerFactory.newInstance();
//            Transformer transformer = transformerFactory.newTransformer();
//            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
//            transformer.setOutputProperty("{http:xml.apache.org/xslt}indent-amount",
//            																	 "4");
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


	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public String getFileName() {
		String filename = "JiraPlugin.jar";
		return filename;
	}
	
	@Override
	public String getName() {
		String name = "JIRA";
		return name;
	}
	
	@Override
	public void terminate() {
		super.terminate();
		p = null;
		client = null;
		projects = null;
		jiraVersions = null;
		jiraComponents = null;
		issueTypes = null;
		priorities = null;
		statuses = null;		
		actions = null;
		issues = null;
		comments = null;
	}
	
	public void initializeRPC(){
		System.out.println(this.variables.get("host"));
		System.out.println(this.variables.get("centralengineport"));
		try{			
			XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
			
			configuration.setServerURL(new URL("http://"+this.variables.get("host")+
					":"+this.variables.get("centralengineport")));
			configuration.setBasicPassword(variables.get("password"));
	        configuration.setBasicUserName(variables.get("user"));
			client = new XmlRpcClient();
			client.setConfig(configuration);
			System.out.println("Client initialized: "+client);
			}
		catch(Exception e){
			System.out.println("Could not conect to "+
		this.variables.get("host")+" :"+this.variables.get("centralengineport")+
		"for RPC client initialization");
			}
		}
		
//	public void initializeSFTP(){
//		try{
//			JSch jsch = new JSch();
//            String user = variables.get("user");
//            Session session = jsch.getSession(user, variables.get("host"), 22);
//            session.setPassword(variables.get("password"));
//            Properties config = new Properties();
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
	
	/**
	 * Jira login method 
	 * Sends login request to Jira via CE & displays confirmation/error message
	 * If login sucessful, swicthes from the login interface 
	 * to the Jira plugin interface and fills in the project combo list for the user
	 */
	public void JiraLogin(){
		try {
			System.out.println("Attempting to login on the server...");
			HashMap params = new HashMap();
			params.put("command", "login");
			params.put("server", p.tfJiraServer.getText());			
			params.put("user", p.tfUsername.getText());
			params.put("passwd", new String(p.tfPassword.getPassword()));	
			Object ob =  client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			Object[] result=null;
			try{result = (Object[])ob;}
			catch(Exception e){
				e.printStackTrace();
				System.out.println(ob);}

			if (result != null){
				projects = result;
				
				p.init();
				p.showPanel(JiraPanel.JIRA_PANEL);
				
				JOptionPane.showConfirmDialog(p, "Jira login successful",
						  					  "Jira Login", JOptionPane.CLOSED_OPTION, 
						  					  JOptionPane.INFORMATION_MESSAGE);
				
				System.out.println("Login successful");	
//				printResult(projects);

				this.p.setComboValues(p.cbProjects, getProperty(projects,"name"));	
				
				jiraElements.put(PROJECT_FIELD,projects);
				jiraElements.put(TYPE_FIELD,JiraGetIssueTypes());
				jiraElements.put(PRIORITY_FIELD, JiraGetPriorities());
				jiraElements.put(STATUS_FIELD, JiraGetStatuses());				
				}
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Login failed");
			JOptionPane.showConfirmDialog(p, "Login failed with error:\n "+e.getMessage(), 
					   "Jira Login", JOptionPane.CLOSED_OPTION,
					  		   JOptionPane.WARNING_MESSAGE);
			terminate();
//			e.printStackTrace();
		}
	}
	
	/**
	 * Jira Get issue types method triggered on login to the jira server
	 * Sends request to Jira to list issue types
	 *
	 * @return array of issuetypes; 
	 * each object in the array is a HashMap that describes an issue type
	 */
	public Object[] JiraGetIssueTypes(){				
		try {
			System.out.println("\n\t - getting issue types");
			HashMap<String,String> params = new HashMap();
			params.put("command", "getissuetypes");
			params.put("server", p.tfJiraServer.getText());
			params.put("user", p.tfUsername.getText());

			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (result!=null){									
				issueTypes = result;
//				printResult(issueTypes);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return issueTypes;
	}
	
	/**
	 * Jira Get priorities types method triggered on login to the jira server
	 * Sends request to Jira to list priorities 
	 */
	/**
	 * @return array list of priorities
	 * each object in the array is a HashMap that describes a priority
	 */
	public Object[] JiraGetPriorities(){				
		try {
			System.out.println("\n\t - getting priorities");
			HashMap<String,String> params = new HashMap();
			params.put("command", "getpriorities");
			params.put("server", p.tfJiraServer.getText());
			params.put("user", p.tfUsername.getText());
			
			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (result != null){
				priorities = result;
//				printResult(priorities);
			}		
			
		} catch (Exception e) {
			e.printStackTrace();
		}
		return priorities;
	}	
	
	/**
	 * Jira Get statuses method triggered on login to the jira server
	 * Sends request to Jira to list the available statuses - 
	 * The statuses are used only at issue creation
	 * @return array of statuses; 
	 * each object in the array is a HashMap that describes a status
	 * 
	 */
	public Object[] JiraGetStatuses(){				
		try {
			System.out.println("\n\t - getting statuses");
			HashMap<String,String> params = new HashMap();
			params.put("command", "getstatuses");
			params.put("server", p.tfJiraServer.getText());
			params.put("user", p.tfUsername.getText());
			
			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (result!=null){		
				statuses = result;
//				printResult(statuses);
				}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return statuses;
	}
	
	/**
	 * Jira Get Versions method
	 * Sends request to Jira to list versions for the project given as argument 
	 * @param projInd - the project index selected by user from the ComboBox
	 * @return array of versions or null if none are defined; 
	 * each object in the array is a HashMap that describes a version
	 * TODO: add support for released/ unreleased versions
	 */
	public Object[] JiraGetVersions(int projInd){
		Object[] versions  = null;
//		System.out.println(projects);
		HashMap project = (HashMap) projects[projInd];
		String projKey = (String) project.get("key");		
		try {
			System.out.println("\n\t - attempting to get versions list for project "+projKey);
			HashMap<String,String> params = new HashMap();
			params.put("command", "getversions");
			params.put("server", p.tfJiraServer.getText());		
			params.put("user", p.tfUsername.getText());
			params.put("project", projKey);			
			
			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (!result.equals("empty")){
				versions = result;
//				System.out.println("\n Versions");
//				printResult(versions);
				jiraElements.put(VERSIONS_FIELD, versions);
			}			
		} catch (Exception e) {
//			e.printStackTrace();
			return versions;
		}
		return versions;
	}

	/**
	 * Jira Get Components method
	 * Sends request to Jira to list components for the project given as argument	 
	 * @param projInd - the index of the project selected by user in the ComboBox
	 * @return array of components or null if none are defined; 
	 * each object in the array is a HashMap that describes a component
	 */
	public Object[] JiraGetComponents(int projInd){		
		HashMap project = (HashMap) projects[projInd];
		String projKey = (String) project.get("key");
		Object[] components = null;
		try {
			System.out.println("\n\t - attempting to get components list for project "+projKey);
			HashMap<String,String> params = new HashMap();
			params.put("command", "getcomponents");
			params.put("server", p.tfJiraServer.getText());		
			params.put("user", p.tfUsername.getText());
			params.put("project", projKey);	
			
			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (!result.equals("empty")){
				components  = result;
//				System.out.println("\n Components");
//				printResult(components);
				jiraElements.put(COMPONENTS_FIELD, components);
			}
			
		} catch (Exception e) {			
			return components;
		}
		return components;
	}
	
	/**
	 * Jira Get Issues method 
	 * Sends request to Jira to list issues for the project given as argument	 
	 * @param projInd - index of the project selected by user in the ComboBox
	 */
	public void JiraGetIssues(int projInd){
		HashMap project = (HashMap) projects[projInd];
		String projKey = (String) project.get("key");					
		issues = JiraGetIssues("project="+projKey);
	}	
	
	/**
	 * Jira Get Issues method 
	 * Sends request to Jira to list components for the project given as argument	 
	 * @param projInd - project selected from ComboBox
	 * @param optInd - version OR component index selected from ComboBox
	 * @param modifier - type of option: version or component
	 * @return list of issue objects (each issue object is a HashMap)
	 * TODO: improve filter to take into account the version types (released/unreleased/fixVersion/affectsVersions)
	 */
	public List JiraGetIssues(int projInd, int optInd, String modifier){
		HashMap project = (HashMap) projects[projInd];
		String projKey = (String) project.get("key");		
		String query = "";
		switch (modifier){
			case JiraPanel.AFFECTS_VERSION:				
				HashMap ver = (HashMap) jiraVersions[optInd];
				String verKey = (String) ver.get("id");
				query = "project="+projKey+" AND "+JiraPanel.AFFECTS_VERSION+"="+verKey;				
				break;
			case JiraPanel.COMPONENT:		
				HashMap comp = (HashMap) jiraComponents[optInd];
				String compKey = (String) comp.get("id");
				query = "project="+projKey+" AND "+JiraPanel.COMPONENT+"="+compKey;				
				break;
		}
		issues = JiraGetIssues(query);
		return issues;
	}
	
	/**
	 * Jira Get Issues method 
	 * Sends request to Jira to list components by query
	 * @param query - query to retrieve issues from the Jira server
	 * @return list of issue objects (each issue object is a HashMap)
	 */
	public List JiraGetIssues(String query){
		HashMap<String,String> params = new HashMap();
		params.put("command", "getissues");
		params.put("server", p.tfJiraServer.getText());		
		params.put("user", p.tfUsername.getText());
		params.put("query", query);
		try {
			System.out.println("\n\t - attempting to get issues by query "+hashToString(params));			
			Object[] rawIssues = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (rawIssues != null){
			    issues = new LinkedList(Arrays.asList(rawIssues));
			    Iterator it = issues.iterator();
//				printResult(issues);
				p.setTableModel(issues,ISSUE_FIELD_NAMES);				
			}
		} catch (Exception e) {
			System.out.println("Issue list is empty or there was an error while fetching issues.");
			System.out.println("If searching issues by query, please make sure the query you entered is correct.");			
//			e.printStackTrace();
		}
		return issues;
	}	
	
	
	/**
	 * Jira Get comments method 
	 * Sends request to Jira to list comments for the issue given as argument
	 * @param issueKey - the issue key for which to get comments as String
	 * @return list of comment objects (each comment object is a HashMap) or null if there are no comments
	 */
	public List JiraGetComments(String issueKey){		
		try {
			System.out.println("\n\t - attempting to get comments for issue "+issueKey);
			HashMap<String,String> params = new HashMap();
			params.put("command", "comments");
			params.put("server", p.tfJiraServer.getText());		
			params.put("user", p.tfUsername.getText());
			params.put("key", issueKey);			
			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (result != null){	
				if (result[0] instanceof String){
					System.out.println(result[0]);
					return null;
				}
			    return Arrays.asList(result);
			}
		} catch (Exception e) {
			System.out.println("There are no comments for this issue or the comment fetch operation failed.");
			return null;
		}
		return null;
	}
	
	/**
	 * Jira Create Issue method 
	 * Sends request to Jira to create a new issue
	 * @param issue - HashMap with data for the issue to be created
	 */
	public void JiraCreateIssue(HashMap issue){	
		try {
			System.out.println("\n\t - attempting to create new issue");
			System.out.println(issue.keySet().toString());
			HashMap params = new HashMap();
			params.put("command", "create");
			params.put("server", p.tfJiraServer.getText());		
			params.put("user", p.tfUsername.getText());
			params.put("issue", removeNullFields(issue));
//			System.out.println(params);
			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (result != null){
				// add the newly created issue to the list of issues
				if (issues!=null){
					issues.add(result[0]);
				}
				else {
					issues = new LinkedList(Arrays.asList(result));  // this is the first issue we get
				}
				// deal with attachments if they have been defined at issue creation
				HashMap h = (HashMap) result[0];
				if (issue.containsKey("attachments")){ // this issue contains attachments					 
					JiraAddAttachment((String)h.get("key"),(Object[]) issue.get("attachments"));
					h.put(JiraPanel.ISSUE_FIELD_ATTACHMENT,issue.get(JiraPanel.ISSUE_FIELD_ATTACHMENT));
				}
				// should update the table
				p.setTableModel(issues,ISSUE_FIELD_NAMES);
			}
		} catch (Exception e) {
			System.out.println("Check Python code. Issue creation failed w message "+e.getMessage());
//			e.printStackTrace();
		}		
	}		
	
	/**
	 * Jira Update Issue method 
	 * Sends request to Jira to update an issue
	 * 	 
	 * @param issue - HashMap with data for the issue to be updated
	 */
	public void JiraUpdateIssue(HashMap issue){
		try {
			System.out.println("\n\t - attempting to update issue "+issue.get("key"));
			HashMap params = new HashMap();
			params.put("command", "update");
			params.put("server", p.tfJiraServer.getText());		
			params.put("user", p.tfUsername.getText());
			params.put("issue", removeNullFields(issue));
			
			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (result != null){
				updateIssue((HashMap) result[0]);
				p.setTableModel(issues,ISSUE_FIELD_NAMES);
			}
		} catch (Exception e) {
			System.out.println("Update failed w message "+e.getMessage());
//			e.printStackTrace();
		}		
	}	
	
	/**
	 * Jira Upload Attachment method 
	 * Uploads an attachment file to the CE server. 
	 * @param h - data of the attachment as a HashMap
	 * @return updated attachment data (the local path is replaced with the remote path) 
	 * TODO : implement ops for delete & download -> no Soap methods available in the Jira Python API :(
	 */
	public HashMap uploadAttach(HashMap h){
		File file = new File((String) h.get("path"));
		String remotePath = variables.get("remoteuserhome")+"/twister/.twister_cache//jira"; 
		try {
			FileInputStream input = new FileInputStream(file);
			
			//c.cd(remotePath);
			//c.put(in, file.getName());
			
			String content = "";
			
			if(input!=null){
                StringBuilder builder = new StringBuilder();
                int ch;
                while((ch = input.read()) != -1){
                    builder.append((char)ch);
                }
                input.close();
                content = builder.toString();
                content = DatatypeConverter.printBase64Binary(content.getBytes());
            }
			
			
			String resp = client.execute("writeFile", new Object[]{remotePath+"/"+file.getName(),content,"w"}).toString();
            if(resp.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,p,"ERROR", resp);
            }
			
			
			
			
			input.close();
			h.put("path", remotePath);
			return h;
		} catch (Exception e){		
			// TODO Auto-generated catch block
			System.out.println("Some error occurred.");
			e.printStackTrace();
			
//			if (e instanceof FileNotFoundException){
//				System.out.println("Local file not found");
//			}
//			if (e instanceof SftpException){
//				SftpException e1 = (SftpException) e;
//				if (e1.id==ChannelSftp.SSH_FX_NO_SUCH_FILE){
//					// probably the remote dir does not exist -> we'll try to create it
//					try {
//						FileInputStream in = new FileInputStream(file);
//						c.mkdir(remotePath);
//						c.cd(remotePath);
//						c.put(in,file.getName());
//						in.close();
//						h.put("path", remotePath);
//						return h;
//					} catch (Exception e2) {
//						// TODO Auto-generated catch block
//						System.out.println("Some error occurred.");
//						e2.printStackTrace();
//					}
//				}
//			}
		}
		return null;
	}
	
	/**
	 * Jira Add Attachments 
	 * Sends request to Jira to add an attachment to an issue
	 * @param issueKey - the key for the issue to add attachment as String
	 * @param attachment - an array of attachment object (each attachment obj is a HashMap) 
	 */
	public void JiraAddAttachment(String issueKey, Object[] attachments){
		HashMap params = new HashMap();
		params.put("command", "attach");
		params.put("server", p.tfJiraServer.getText());
		params.put("user", p.tfUsername.getText());
		params.put("key", issueKey);
		params.put("attachments", attachments);			
		try {
			System.out.println("\n\t - attempting to update attachments of issue "+issueKey);
			
			boolean result = (boolean) client.execute("runPlugin", new Object[]{variables.get("user"),
					getName(),params});
			if (result){
				System.out.println("Attach successful to issue "+issueKey);
			}
		} catch (Exception e) {
			//				e.printStackTrace();
			System.out.println("Attaching for "+issueKey+" failed with error message "+e.getMessage());
		}		
	}	
	
	/**
	 * Jira Update Comment
	 * Sends request to Jira to update a comment or create it if it's a new comment
	 * @param issueKey - key of the issue to which to add the comment (as String)	 
	 * @param comment - HashMap with data for the comment to be created/updated
	 */
	public void JiraUpdateComment(HashMap comment, String issueKey){
		HashMap params = new HashMap();
		
		params.put("server", p.tfJiraServer.getText());
		params.put("user", p.tfUsername.getText());
		params.put("body", (String) comment.get("body"));
		if (comment.containsKey("id")){ // this is an update			
			try {
				System.out.println("\n\t - attempting to update comment with id "+comment.get("id"));
				params.put("command", "editcomment");
				params.put("id", (String) comment.get("id"));				
								
				Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
						 getName(),params});
				if (result != null){
					System.out.println("Comment edited.");
				}
			} catch (Exception e) {
//				e.printStackTrace();
				System.out.println("Comment update for issue "+issueKey+" failed with error message "+e.getMessage());
			}
		}
		else{ // this is create
			try {
				System.out.println("\n\t - attempting to create a new comment for issue "+issueKey);
				params.put("command", "comment");
				params.put("key", issueKey);				
								
				Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
						 getName(),params});
				if (result != null){
					System.out.println("Comment creation successful.");
				}
			} catch (Exception e) {
//				e.printStackTrace();
				System.out.println("Comment create for issue "+issueKey+" failed with error message "+e.getMessage());
			}
		}
				
	}
		
	/**
	 * Jira Get available actions method 
	 * Sends request to Jira to list the available action for the issue
	 * based on its current status.
	 * The status update for an issue cannot be done directly by assigning another status.
	 * It can only be done by performing one of the available actions in the issue workflow.
	 * @param issueKey - the key for the issue to get available actions (as String)
	 * @return array of action objects (each object is a HashMap)
	 */
	public Object[] JiraGetAvailableActions(String issueKey){
//		Object[] actions = null;
		try {
			System.out.println("\n\t - getting available actions for issue "+issueKey);
			HashMap params = new HashMap();
			params.put("command", "actions");
			params.put("server", p.tfJiraServer.getText());			
			params.put("user", p.tfUsername.getText());
			params.put("key", issueKey);
			
			Object[] result = (Object[]) client.execute("runPlugin", new Object[]{variables.get("user"),
					 getName(),params});
			if (result!=null){									
				actions = result;
			}
		} catch (Exception e) {
//			e.printStackTrace();
			System.out.println("There was an error getting available actions for issue "+issueKey);
		}
		return actions;
	}

// ----------------------  UTILITY METHODS ----------------------
	
	/**
	 * This method returns the value of the field given as parameter. 
	 * For fields whose values are given as ids, the method return the 
	 * corresponding name.
	 * @param object - HashMap with object data as (key, value) pairs
	 * @param field - the name of the key to retrieve from the HashMap
	 * @return a String representing the value of the issue field
	 */
	public String getFieldValue(HashMap object, String field){
		String elementName = field;
		String key = "id";
		if (field.equals("fixVersions")||field.equals("affectsVersions"))
			elementName = VERSIONS_FIELD;
		if (field.equals(PROJECT_FIELD))
			key = "key";
//		System.out.println(elementName);
//		System.out.println(propName);
		if (object.get(field)==null)
			return "";	
		if (Arrays.asList(ID_FIELDS).contains(field)){
			if (object.get(field) instanceof Object[]){
				Object[] vals = (Object[]) object.get(field);
				HashMap h = (HashMap) vals[0];
				String s = (String) h.get("name");
				for (int k=1;k<vals.length;k++){
					h = (HashMap) vals[k];
					s = s + "; "+ h.get("name");
				}
				return s;
			} 
			else {
				String val = (String) object.get(field);
				Object[] elementList = (Object[]) jiraElements.get(elementName);
				if (elementList!=null){
					for (Object o: elementList){
						HashMap h = (HashMap) o;
						if (h.get(key).equals(val)){
							return (String) h.get("name");
						}
					}
				}
				return ""; // this is where I get if either elementList is null ->  
				// OR there is no object in elementList that matches the value of key							
			}
		}
		
		if (object.get(field) instanceof Object[]){
			Object[] vals = (Object[]) object.get(field);
			Object val = vals[0];
			if (val instanceof String){
				String s = (String) vals[0];
				for (int k=1; k<vals.length; k++){
					s = s + "; " + vals[k];
				}
				return s;	
			} 
		}
		
		if (object.get(field) instanceof List){
			List vals = (List) object.get(field);
			HashMap val = (HashMap) vals.get(0);
			String s = (String) val.get("filename");
			for (int k=1; k<vals.size(); k++){
				HashMap h = (HashMap) vals.get(k);
				s = s + "; " + h.get("filename");				
			}
			return s;	
		}
		
		if (object.get(field) instanceof String){
			String val = (String) object.get(field);
			if (!val.equals("[]")){
				return val;
			}			
		}		
		return ""; // this is where I get if I don't return anywhere else ->
		// I return "" if the value is "[]" or the object is of unknown type
	}
	
	/**
	 * This method returns a String array of the values of a given property 
	 * of the objects in an array.
	 * @param objectList - the array of objects where each object is a HashMap (property, value) pairs
	 * @param propName - the name of the property to retrieve from the HashMap (String)
	 * @return a String array of the values of that property for all objects
	 */
	public String[] getProperty(Object[] objectList, String propName){
		String[] result = new String[objectList.length];
		int i = 0;
		for (Object h: objectList){
			HashMap hmap = (HashMap) h; 
			result[i]=(String) hmap.get(propName);		
			i++;
		}
		return result;
	}
	
	/**
	 * This method returns an issue object from an array of issues
	 * @param key - key of the issue to search in the array (String)
	 * @return a HashMap representing the issue object
	 */	
	public HashMap getIssueByKey(String key){
		Iterator it = issues.iterator();
		while (it.hasNext()){
			HashMap i = (HashMap) it.next();
			if (i.get("key").equals(key)){
				return i;				
			}
		}
		return null;
	}

	/**
	 * This method updates an issue in the array of issues
	 * @param issue - issue object to update (HashMap)
	 */	
	public void updateIssue(HashMap issue){
		Iterator it = issues.iterator();
		while (it.hasNext()){
			HashMap i = (HashMap) it.next();
			if (i.get("key").equals(issue.get("key"))){
				int index = issues.indexOf(i);
				issues.set(index, issue);
			}
		}
	}
	
	/**
	 * Getter method for projects
	 * @return array of project objects (HashMaps)
	 */	
	public Object[] getProjects() {
		return projects;
	}
	/**
	 * Getter method for issue types
	 * @return array of issue type objects (HashMaps)
	 */	
	public Object[] getIssueTypes() {
		return issueTypes;
	}
	/**
	 * Getter method for priority types
	 * @return array of priority objects (HashMaps)
	 */	
	public Object[] getPriorities() {
		return priorities;
	}	
	/**
	 * Getter method for status types
	 * @return array of status objects (HashMaps)
	 */	
	public Object[] getStatuses() {
		return statuses;
	}
	/**
	 * Getter method for available actions
	 * @return array of available action objects (HashMaps)
	 */	
	public Object[] getActions() {
		return actions;
	}
	/**
	 * Setter method for versions
	 * @param array of version objects (array of HashMaps)
	 */	
	public void setVersions(Object[] ver){
		jiraVersions = ver;
	}	
	/**
	 * Getter method for versions
	 * @return array of version objects (array of HashMaps)
	 */
	public Object[] getJiraVersions(){
		return jiraVersions;
	}	
	/**
	 * Setter method for components
	 * @param array of component objects (array of HashMaps)
	 */
 	public void setComponents(Object[] comp){
		jiraComponents = comp;
	} 	
 	/**
	 * Getter method for components
	 * @return array of component objects (array of HashMaps)
	 */
	public Object[] getJiraComponents(){
		return jiraComponents;
	}

	/**
	 * This method returns the id of an object from a list of objects 
	 * given the object's name
	 * @param objList - array of objects (array of HashMaps)
	 * @param name - name of the object we're looking for
	 * @return the id of the object (as String) or an empty String if name not found
	 */
	public String getIdFromName(Object[] objList, String name){
		for (Object o: objList){
			HashMap h = (HashMap) o;
			if (h.get("name").equals(name)){
//				System.out.println(name+" -> id = "+h.get("id"));
				return (String) h.get("id");
			}
		}
		return "";
	}
	
	/**
	 * This method returns the id of an object from a list of objects 
	 * given the object's name and the object list's type
	 * @param elementName - the type of object we're looking for (as String) eg: "priority", "type", etc.
	 * @param name - name of the object we're looking for
	 * @return the id of the object (as String) or an empty String if name not found
	 */
	public String getIdFromName(String elementName, String name){
		String key = "id";
		if (elementName.equals("project"))
			key = "key";
		Object[] elements = (Object[]) jiraElements.get(elementName);
		if (elements!=null){
			int i=0;
			for (Object o: elements){
				HashMap h = (HashMap) o;
				if (name.equals(h.get("name"))){
//					System.out.println("Found object "+h.get("name"));
					return (String) h.get(key);					
				}
			}
		}
		return "";
	}	
	
	/**
	 * This method returns a subset of objects from a list of objects given a string array of names 
	 * @param elementName - the type of objects we're looking for (as String) eg: "priority", "type", etc.
	 * @param names - array of names of the objects we're looking for (array of String)
	 * @return an array of objects (array of HashMaps) or null if names not found
	 */
	public Object[] getObjects(String elementName, String[] names){
		ArrayList res = new ArrayList();
		Object[] elements = (Object[]) jiraElements.get(elementName);
		if (elements!=null){			
			for (Object o: elements){
				HashMap h = (HashMap) o;
				if (Arrays.asList(names).contains(h.get("name"))){
					res.add(o);
					System.out.println("Found object "+h.get("name"));
				}
			}
			return res.toArray();
		}
		return null;				
	}
	
	/**
	 * This method returns a String representation of a HashMap object 
	 * Used to generate String queries.
	 * @param obj - the HashMap object
	 * @return a String representation of the HashMap obj
	 */
	public String hashToString(HashMap obj){
		String res = "";
		Object[] fields = obj.keySet().toArray();
		res = fields[0]+"="+obj.get(fields[0]);
		for (int i=1; i<fields.length; i++){
			String key = (String) fields[i];			
			if (obj.get(key) instanceof String){
				res = res+"&"+key+"="+obj.get(key);
			}
			if (obj.get(key) instanceof Object[]){
				Object[] list = (Object[]) obj.get(key);
				for (int k=0; k<list.length; k++){
					HashMap h = (HashMap) list[k];
					res = res+"&"+key+"="+h.get("id");
				}
			}			
		}
		return res;
	}
	
	/**
	 * This method removes the null fields in a HashMap object.
	 * This is used because null values cause problems when passed by XML-RPC 
	 * @param obj - the HashMap object
	 * @return the HashMap object with all null entries removed
	 */	
	public HashMap removeNullFields(HashMap obj){
		for (Object o: obj.keySet().toArray()){
			String key = (String) o;
			if (obj.get(key)==null){
				obj.remove(key);
			}			
		}
		return obj;
	}
	
	/**
	 * This method prints a List object.
	 * @param obj - List object to print out
	 */
	public void printResult(List obj){
	    //get an iterator
	    Iterator itr = obj.iterator();
	    //iterate through list created from Array
	    while(itr.hasNext()){
	      HashMap h = (HashMap) itr.next();
	      printHashMap(h);
	    }
	}
	
	/**
	 * This method prints an array of HashMap objects.
	 * @param obj - the array of objects to print out
	 */
	public void printResult(Object[] obj){
		for (int i=0; i<obj.length; i++){
			HashMap h = (HashMap) obj[i];
			printHashMap(h);
		}
	}
	
	/**
	 * This method prints a HashMap objects.
	 * @param h - the HashMap object to print out
	 */
	public void printHashMap(HashMap h){
		Object[] keys = h.keySet().toArray();
		for (Object k: keys){
			System.out.print(k+" : "+h.get(k));
			System.out.print("\t");
			if (h.get(k) instanceof Object[]){
				Object[] l = (Object[]) h.get(k);
				System.out.println(l.length);					
			}
			System.out.println();
		}
	}	
	
	
	
// ---------------------- END UTILITY METHODS ----------------------		
	/**
	 * The main method used for debugging
	 * @param args[] - standard array of arguments
	 */
	public static void main(String args[]){
		
		variables = new Hashtable<String, String>();
		variables.put("user", "tscguest");
		variables.put("password", "tscguest");
		variables.put("host", "11.126.32.9");
		variables.put("centralengineport", "8000");
		variables.put("remoteuserhome", "/home/tscguest");
		
		JiraPlugin plugin = new JiraPlugin();
		isApplet = false;
		plugin.init(null, null, variables, null, null);
	
	}
}

