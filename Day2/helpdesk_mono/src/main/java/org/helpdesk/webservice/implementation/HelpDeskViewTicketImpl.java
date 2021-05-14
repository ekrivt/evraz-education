package org.helpdesk.webservice.implementation;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.HttpHeaders;

import org.helpdesk.commons.exception.ServiceInvocationException;
import org.helpdesk.webservice.extension.HelpDeskViewTicket;
import org.helpdesk.webservice.support.HelpDeskViewTicketHelper;
import org.helpdesk.webservice.request.NoteRequest;
import org.helpdesk.webservice.request.ResolveRequest;
import org.helpdesk.webservice.response.NoteResponse;
import org.helpdesk.webservice.response.ResolveResponse;
import org.helpdesk.webservice.response.ViewAllTicketResponse;
import org.helpdesk.webservice.response.ViewTicketResponse;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.BeanFactory;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;

@Component
@Path("/HelpDeskViewTicket")
public class HelpDeskViewTicketImpl implements HelpDeskViewTicket {

	HelpDeskViewTicketHelper helper=null;

	
	@POST
	@Consumes({"application/xml", "application/json"})
	@Produces({"application/json"})
	@Path("/addNote")
	public NoteResponse addNote(@Context HttpHeaders headers, NoteRequest request)
			throws ServiceInvocationException {
		NoteResponse response=new NoteResponse();
		response=helper.addnote(request);
		return response;
	}
	
	@POST
	@Consumes({"application/xml", "application/json"})
	@Produces({"application/json"})
	@Path("/resolveTicket")
	public ResolveResponse resolveTicket(@Context HttpHeaders headers, ResolveRequest request)
			throws ServiceInvocationException {
		 ResolveResponse response=new  ResolveResponse();
		response=helper.resolveTicket(request);
		return response;
	}
	
	@Override
	@GET
	@Consumes({"application/xml", "application/json"})
	@Produces({"application/json"})
	@Path("/viewAllTicket/")
	public ViewAllTicketResponse viewAllTicket(@Context HttpHeaders headers)
			throws ServiceInvocationException {
		ViewAllTicketResponse response=helper.getAllTicket();
		return response;
	}
	
	@GET
	@Consumes({"application/xml", "application/json"})
	@Produces({"application/json"})
	@Path("/viewUsersTicket/{userId}")
	public ViewAllTicketResponse viewUsersTicket(@Context HttpHeaders headers,@PathParam("userId")String  userId)
			throws ServiceInvocationException {
		ViewAllTicketResponse response=helper.getAllTicket(userId);
		return response;
	}
	
	@Override
	@GET
	@Consumes({"application/xml", "application/json"})
	@Produces({"application/json"})
	@Path("/viewTicket/{ticketId}")
	public ViewTicketResponse viewTicket(@Context HttpHeaders headers, @PathParam("ticketId")String  ticketId)
			throws ServiceInvocationException {
		ViewTicketResponse response=helper.getTicket(ticketId);
		return response;
	}


	@Override
	public void setBeanFactory(BeanFactory arg0) throws BeansException {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setApplicationContext(ApplicationContext arg0)
			throws BeansException {
		// TODO Auto-generated method stub
		
	}

	/**
	 * @return the helper
	 */
	public HelpDeskViewTicketHelper getHelper() {
		return helper;
	}

	/**
	 * @param helper the helper to set
	 */
	public void setHelper(HelpDeskViewTicketHelper helper) {
		this.helper = helper;
	}




}
