---
title: "6.2. Create and use Quick Suite Spaces with default chat agent"
weight: 67
---

The [spaces](https://aws.amazon.com/quick/spaces/) capability in Quick allows you to create a collection of data and resources for your particular team. You can use spaces to simply upload and organize files, dashboards, topics, knowledge bases, and application actions into a unified and customizable knowledge center for your team, that enables highly contextual conversations and is designed to scale across personal, team, and cross-team use cases. Multiple people on the team can contribute to the knowledge inside a space streamlining information discovery.

[Quick chat agents](https://aws.amazon.com/quick/chat-agents/) are AI-powered conversational interfaces that provide instant access to your organization’s knowledge base. Quick offers two types of chat agents -
  * A general chat agent to get answers to your questions related to data across your organization
  * A custom chat agents that you can create and share by restricting access to specific data sources and actions and adding specific instructions for an even more contextual experience, specific to your team or organization.

In this section, you will create a Quick Suite space for risk metrics assessment and use that with the default chat agent and ask questions.

1. From the top left bar, select **Explore** and then choose **Spaces**. Next, select **Create space**.

![Create Space](/static/images/FSI-Images/Lab6-Quick-17-Create-space.png)

2. Rename the space to :code[Risk Assessment]{showCopyAction=true}. Then, under **Add knowledge**, first you will add the published dashboard under **Dashboards** and then the `Risk_Metrics` topic under **Topics**.

![Name space and add knowledge](/static/images/FSI-Images/Lab6-Quick-18-Name-space.png)

3. Select **Add knowledge** and then choose **Dashboards**. Select `RiskMetrics_Dashboard` and then select **Add**.

![Add Dashboard](/static/images/FSI-Images/Lab6-Quick-19-Add-dashboard-to-space.png)

4. Next, select **Add knowledge** and then choose **Topics**. Select the `Risk_Metrics` topic and then select **Add**.

![Add Topic](/static/images/FSI-Images/Lab6-Quick-20-Add-Topics-to-space.png)

5. Once completed, you will be able to see the added dashboard and topic under **All knowledge** of the `Risk Assessment` space.

![Add Topic](/static/images/FSI-Images/Lab6-Quick-21-Space-view.png)

6. Once the space is created, you will see the default chat option on the right of the screen include `Risk Assessment`space under **Specific data and apps**. If the default chat option is not showing on the right pane, select the chat icon on the top right of the screen.

![Use space in chat](/static/images/FSI-Images/Lab6-Quick-22-Use-Space-in-chat.png)

7. Next, you will add the following question to the chat prompt to analyze the data in the space and select enter:

    :code[Provide details on high-risk loans across different customer segments]{showCopyAction=true}

   The query will generate the analysis of the Risk Assessment data with the details on high-risk loans across different customer segments.

![Default chat](/static/images/FSI-Images/Lab6-Quick-30-Default_chat.png)

Thus, using the knowledge added to the Quick space, you can use the default chat agent to ask natural language questions on the data.

::alert[**Congratulations!** You've successfully analyzed your financial services data using natural language conversations, generating instant insights and summaries, using a default chat agent.]{type=success}