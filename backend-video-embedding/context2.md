This guide shows how you can use the Analyze API to perform open-ended analysis on video content, generating tailored text outputs based on your prompts. This feature provides more customization options than the summarization feature. It supports generating various content types based on your prompts, including, but not limited to, tables of content, action items, memos, reports, and comprehensive analyses.

The platform provides two distinct methods for retrieving the results of the open-ended analysis:

<AccordionGroup>
  <Accordion title="Streaming responses">
    Streaming responses deliver text fragments in real-time as they are generated, enabling immediate processing and feedback. This method is the default behavior of the platform and is ideal for applications requiring incremental updates.<br/>
    - **Response format**: A stream of JSON objects in NDJSON format, with three event types:
      - `stream_start`: Marks the beginning of the stream.
      - `text_generation`: Delivers a fragment of the generated text.
      - `stream_end`: Signals the end of the stream.<br/>
    - **Response handling**:
      - Iterate over the stream to process text fragments as they arrive.<br/>
    - **Advantages**:
      - Real-time processing of partial results.
      - Reduced perceived latency.
    - **Use case**: Live transcription, real-time analysis, or applications needing instant updates.
  </Accordion>
  <Accordion title="Non-streaming responses">
    Non-streaming responses deliver the complete generated text in a single response, simplifying processing when the full result is needed.
    - **Response format**: A single string containing the full generated text.
    - **Response handling**:
      - Access the complete text directly from the response.
    - **Advantages**:
      - Simplicity in handling the full result.
      - Immediate access to the entire text.
    - **Use case**: Generating reports, summaries, or any scenario where the whole text is required at once.
  </Accordion>
</AccordionGroup>

This guide provides a complete example. For a simplified introduction with just the essentials, see the [Analyze videos](/v1.3/docs/get-started/quickstart/analyze-videos) quickstart guide.

# Prerequisites

- To use the platform, you need an API key:
     <Steps>
         <Step>
             If you don’t have an account, [sign up](https://playground.twelvelabs.io/) for a free account.
         </Step>
         <Step>
             Go to the [API Key](https://playground.twelvelabs.io/dashboard/api-key) page.
         </Step>
         <Step>
             Select the **Copy** icon next to your key.
         </Step>
     </Steps>
- Ensure the TwelveLabs SDK is installed on your computer:

     <CodeBlocks>
         ```shell Python
         pip install twelvelabs
         ```
         ```shell Node.js
         yarn add twelvelabs-js # or npm install twelvelabs-js
         ```
     </CodeBlocks>

- The videos you wish to use must meet the following requirements:
    - **Video resolution**: Must be at least 360x360 and must not exceed 3840x2160.
    - **Aspect ratio**: Must be one of 1:1, 4:3, 4:5, 5:4, 16:9, 9:16, or 17:9.

    - **Video and audio formats**: Your video files must be encoded in the video and audio formats listed on the <a href="https://ffmpeg.org/ffmpeg-formats.html" target="_blank">FFmpeg Formats Documentation</a> page. For videos in other formats, contact us at [support@twelvelabs.io](mailto:support@twelvelabs.io).
    - **Duration**: Must be between 4 seconds and 60 minutes (3600s). In a future release, the maximum duration will be 2 hours (7,200 seconds).
    - **File size**:  Must not exceed 2 GB.
     If you require different options, contact us at [support@twelvelabs.io](mailto:support@twelvelabs.io).

# Complete example

This complete example shows how to create an index, upload a video, and perform open-ended analysis to generate text based on the content of your video. Ensure you replace the placeholders surrounded by `<>` with your values.

<Tabs>
  <Tab title="Streaming responses">
    <CodeBlocks>
      ```Python Python maxLines=8
      from twelvelabs import TwelveLabs
      from twelvelabs.indexes import IndexesCreateRequestModelsItem
      from twelvelabs.tasks import TasksRetrieveResponse

      # 1. Initialize the client
      client = TwelveLabs(api_key="<YOUR_API_KEY>")

      # 2. Create an index
      index = client.indexes.create(
          index_name="<YOUR_INDEX_NAME>",
          models=[
              IndexesCreateRequestModelsItem(
                  model_name="pegasus1.2", model_options=["visual", "audio"]
              )
          ]
      )
      print(f"Created index: id={index.id}")

      # 3. Upload a video
      task = client.tasks.create(
          index_id=index.id, video_url="<YOUR_VIDEO_URL>")
      print(f"Created task: id={task.id}")

      # 4. Monitor the indexing process
      def on_task_update(task: TasksRetrieveResponse):
          print(f"  Status={task.status}")

      task = client.tasks.wait_for_done(
          sleep_interval=5, task_id=task.id, callback=on_task_update)
      if task.status != "ready":
          raise RuntimeError(f"Indexing failed with status {task.status}")
      print(
          f"Upload complete. The unique identifier of your video is {task.video_id}.")

      # 5. Perform open-ended analysis
      text_stream = client.analyze_stream(
          video_id=task.video_id,
          prompt="<YOUR_PROMPT>",
          # temperature=0.2
      )

      # 6. Process the results
      for text in text_stream:
          if text.event_type == "text_generation":
              print(text.text)
      ```

      ```JavaScript Node.js maxLines=8
      import { TwelveLabs, TwelvelabsApi } from "twelvelabs-js";

      // 1. Initialize the client
      const client = new TwelveLabs({ apiKey: "<YOUR_API_KEY>" });

      // 2. Create an index
      const index = await client.indexes.create({
          indexName: "<YOUR_INDEX_NAME>",
          models: [
              {
                  modelName: "pegasus1.2",
                  modelOptions: ["visual", "audio"],
              },
          ],
      });
      console.log(`Created index: id=${index.id}`);

      // 3. Upload a video
      const createTaskResponse = await client.tasks.create({
          indexId: index.id!,
          videoUrl: "<YOUR_VIDEO_URL>",
      });

      console.log(`Created task: id=${createTaskResponse.id}`);

      // 4. Monitor the indexing process
      const task = await client.tasks.waitForDone(createTaskResponse.id!, {
          sleepInterval: 5,
          callback: (task: TwelvelabsApi.TasksRetrieveResponse) => {
              console.log(`  Status=${task.status}`);
          },
      });

      if (task.status !== "ready") {
          throw new Error(`Indexing failed with status ${task.status}`);
      }
      console.log(
          `Upload complete. The unique identifier of your video is ${task.videoId}`,
      );

      // 5. Perform open-ended analysis
      const textStream = await client.analyzeStream({
          videoId: task.videoId!,
          prompt: "<YOUR_PROMPT>",
          // temperature: 0.2,
      });

      // 6. Process the results
      for await (const text of textStream) {
          if ("text" in text) {
              console.log(text.text!);
          }
      }
      ```

    </CodeBlocks>
  </Tab>
  <Tab title="Non-streaming responses">
    <CodeBlocks>
      ```Python Python maxLines=8
      from twelvelabs import TwelveLabs
      from twelvelabs.indexes import IndexesCreateRequestModelsItem
      from twelvelabs.tasks import TasksRetrieveResponse

      # 1. Initialize the client
      client = TwelveLabs(api_key="<YOUR_API_KEY>")

      # 2. Create an index
      index = client.indexes.create(
          index_name="<YOUR_INDEX_NAME>",
          models=[
              IndexesCreateRequestModelsItem(
                  model_name="pegasus1.2", model_options=["visual", "audio"]
              )
          ]
      )
      print(f"Created index: id={index.id}")

      # 3. Upload a video
      task = client.tasks.create(
          index_id=index.id, video_url="<YOUR_VIDEO_URL>")
      print(f"Created task: id={task.id}")

      # 4. Monitor the indexing process

      def on_task_update(task: TasksRetrieveResponse):
          print(f"  Status={task.status}")

      task = client.tasks.wait_for_done(
          sleep_interval=5, task_id=task.id, callback=on_task_update)
      if task.status != "ready":
          raise RuntimeError(f"Indexing failed with status {task.status}")
      print(
          f"Upload complete. The unique identifier of your video is {task.video_id}.")

      # 5. Perform open-ended analysis
      text = client.analyze(
        video_id=task.video_id,
        prompt="<YOUR_PROMPT>",
        # temperature=0.2
      )

      # 6. Process the results
      print(f"{text.data}")

      ```

      ```JavaScript Node.js maxLines=8
      // 1. Initialize the client
      const client = new TwelveLabs({ apiKey: "<YOUR_API_KEY>" });

      // 2. Create an index
      const index = await client.indexes.create({
          indexName: "<YOUR_INDEX_NAME>",
          models: [
              {
                  modelName: "pegasus1.2",
                  modelOptions: ["visual", "audio"],
              },
          ],
      });
      console.log(`Created index: id=${index.id}`);

      // 3. Upload a video
      const createTaskResponse = await client.tasks.create({
          indexId: index.id!,
          videoUrl: "<YOUR_VIDEO_URL>",
      });

      console.log(`Created task: id=${createTaskResponse.id}`);

      // 4. Monitor the indexing process
      const task = await client.tasks.waitForDone(createTaskResponse.id!, {
          sleepInterval: 5,
          callback: (task: TwelvelabsApi.TasksRetrieveResponse) => {
              console.log(`  Status=${task.status}`);
          },
      });

      if (task.status !== "ready") {
          throw new Error(`Indexing failed with status ${task.status}`);
      }
      console.log(
          `Upload complete. The unique identifier of your video is ${task.videoId}`,
      );

      // 5. Perform open-ended analysis
      const text = await client.analyze({
      videoId: task.videoId!,
      prompt: "<YOUR_PROMPT>",
      // temperature: 0.2,
      });

      // 6. Process the results
      console.log(`${text.data}`);
      ```

    </CodeBlocks>
  </Tab>
</Tabs>

# Step-by-step guide

<Tabs>
  <Tab title="Python">
    <Steps>
      <Step title="Import the SDK and initialize the client">
          Create a client instance to interact with the TwelveLabs Video Understanding Platform.<br/>
          **Function call**: You call the [constructor](/v1.3/sdk-reference/python/the-twelve-labs-class#the-initializer) of the `TwelveLabs` class.<br/>
          **Parameters**:
          - `api_key`: The API key to authenticate your requests to the platform.<br/>

          **Return value**: An object of type `TwelveLabs` configured for making API calls.
      </Step>

      <Step title="Create an index">
          Indexes store and organize your video data, allowing you to group related videos. Create one before uploading videos.<br/>
          **Function call**: You call the [`indexes.create`](/v1.3/sdk-reference/python/manage-indexes#create-an-index) function.<br/><br/>
          **Parameters**:
          - `index_name`: The name of the index.
          - `models`: An array specifying your model configuration.

          See the [Indexes](/v1.3/docs/concepts/indexes) page for more details on creating an index and specifying the model configuration.<br/>

          **Return value**: An object containing, among other information, a field named `id` representing the unique identifier of the newly created index.
      </Step>
      <Step title="Upload videos">
          To perform any downstream tasks, you must first upload your videos, and the platform must finish indexing them.<br/>
          **Function call**: You call the [`tasks.create`](/v1.3/sdk-reference/python/upload-videos#create-a-video-indexing-task) function.<br/>
          **Parameters**:
          - `index_id`: The unique identifier of your index.
          - `video_url` or `video_file`: The publicly accessible URL or the path of your video file.<br/>

          **Return value**: An object of type `TasksCreateResponse` that you can use to track the status of your video upload and indexing process. This object contains, among other information, the following fields:
          - `id`: The unique identifier of your video indexing task.
          - `video_id`: The unique identifier of your video.
          <Note title="Note">
              You can also upload multiple videos in a single API call. For details, see the [Cloud-to-cloud integrations](/v1.3/docs/advanced/cloud-to-cloud-integrations) page.
          </Note>
      </Step>

      <Step title="Monitor the indexing process">
          The platform requires some time to index videos. Check the status of the video indexing task until it's completed.<br/>
          **Function call**: You call the [`tasks.wait_for_done`](/v1.3/sdk-reference/python/upload-videos#wait-for-a-video-indexing-task-to-complete) function.<br/>
          **Parameters**:
          - `sleep_interval`: The time interval, in seconds, between successive status checks. In this example, the method checks the status every five seconds.
          - `task_id`: The unique identifier of your video indexing task.
          - `callback`:  A callback function that the SDK executes each time it checks the status.<br/>

          **Return value**: An object of type `TasksRetrieveResponse` containing, among other information, a field named `status` representing the status of your task. Wait until the value of this field is `ready`.
      </Step>
      <Step title="Perform open-ended analysis">
        <Tabs>
          <Tab title="Streaming responses">
            **Function call**: You call the [`analyze_stream`](/v1.3/sdk-reference/python/analyze-videos#open-ended-analysis-with-streaming-responses) method.<br/>
            **Parameters**:
            - `video_id`: The unique identifier of the video for which you want to generate text.
            - `prompt`: A string that guides the model on the desired format or content. The maximum length of a prompt is 2,000 tokens.
            - _(Optional)_ `temperature`: A number that controls the randomness of the text. A higher value generates more creative text, while a lower value produces more deterministic text.<br/>

            **Return value**: An object that handles streaming HTTP responses and provides an iterator interface allowing you to process text fragments as they arrive. The maximum length of the response is 4,096 tokens.<br/>
          </Tab>
          <Tab title="Non-streaming responses">
            **Function call**: You call the [`analyze`](/v1.3/sdk-reference/python/analyze-videos#open-ended-analysis) method.<br/>
            **Parameters**:
            - `video_id`: The unique identifier of the video for which you want to generate text.
            - `prompt`: A string that guides the model on the desired format or content. The maximum length of a prompt is 2,000 tokens.
            - _(Optional)_ `temperature`: A number that controls the randomness of the text. A higher value generates more creative text, while a lower value produces more deterministic text.<br/>

            **Return value**: An object containing a field named `data` of type `string` representing the generated text. The maximum length of the response is 4,096 tokens.<br/>
          </Tab>
        </Tabs>
        <Note title="Note">
          If you encounter timeout errors, increase the `timeout` parameter when you [initialize](/sdk-reference/python/the-twelve-labs-class#the-initializer) the `TwelveLabs` client. The default timeout is 60 seconds, which may not be sufficient for complex prompts, especially with non-streaming responses..
        </Note>
      </Step>
      <Step title="Process the results">
        <Tabs>
          <Tab title="Streaming responses">
            Use a loop to iterate over the stream. Inside the loop, handle each text fragment as it arrives.
          </Tab>
          <Tab title="Non-streaming responses">
            This example prints the generated text to the standard output.
          </Tab>
        </Tabs>
      </Step>
    </Steps>
  </Tab>
  <Tab title="Node.js">
    <Steps>
      <Step title="Import the SDK and initialize the client">
          Create a client instance to interact with the TwelveLabs Video Understanding Platform.<br/>
          **Function call**: You call the [constructor](/v1.3/sdk-reference/node-js/the-twelve-labs-class#the-constructor) of the `TwelveLabs` class.<br/>
          **Parameters**:
          - `apiKey`: The API key to authenticate your requests to the platform.<br/>

          **Return value**: An object of type `TwelveLabs` configured for making API calls.
      </Step>

      <Step title="Create an index">
          Indexes store and organize your video data, allowing you to group related videos. Create one before uploading videos.<br/>
          **Function call**: You call the [`indexes.create`](/v1.3/sdk-reference/node-js/manage-indexes#create-an-index) function.<br/>
          **Parameters**:
          - `indexName`: The name of the index.
          - `models`: An array specifying your model configuration.

          See the [Indexes](/v1.3/docs/concepts/indexes) page for more details on creating an index and specifying the model configuration.<br/>

          **Return value**: An object containing, among other information, a field named `id` representing the unique identifier of the newly created index.
      </Step>
      <Step title="Upload videos">
          To perform any downstream tasks, you must first upload your videos, and the platform must finish indexing them.<br/>
          **Function call**: You call the [`tasks.create`](/v1.3/sdk-reference/node-js/upload-videos#create-a-video-indexing-task) function.<br/>
          **Parameters**:
          - `indexId`: The unique identifier of your index.
          - `videoUrl` or `videoFile`: The publicly accessible URL or the path of your video file.<br/>

          **Return value**: An object of type `TasksCreateResponse` that you can use to track the status of your video upload and indexing process. This object contains, among other information, the following fields:
          - `id`: The unique identifier of your video indexing task.
          - `videoId`: The unique identifier of your video.
          <Note title="Note">
              You can also upload multiple videos in a single API call. For details, see the [Cloud-to-cloud integrations](/v1.3/docs/advanced/cloud-to-cloud-integrations) page.
          </Note>
      </Step>
      <Step title="Monitor the indexing process">
          The platform requires some time to index videos. Check the status of the video indexing task until it's completed.<br/>
          **Function call**: You call the [`tasks.waitForDone`](/v1.3/sdk-reference/node-js/upload-videos#wait-for-a-video-indexing-task-to-complete) function.<br/>
          **Parameters**:
          - `sleepInterval`: The time interval, in seconds, between successive status checks. In this example, the method checks the status every five seconds.
          - `taskId`: The unique identifier of your video indexing task.
          - `callback`:  A callback function that the SDK executes each time it checks the status.<br/>

          **Return value**: An object of type `TasksRetrieveResponse` containing, among other information, a field named `status` representing the status of your task. Wait until the value of this field is `ready`.
      </Step>
      <Step title="Perform open-ended analysis">
        <Tabs>
          <Tab title="Streaming responses">
            **Function call**: You call the [`analyzeStream`](/v1.3/sdk-reference/node-js/analyze-videos#open-ended-analysis-with-streaming-responses) method.<br/>

            **Parameters**:
            - `videoId`: The unique identifier of the video for which you want to generate text.
            - `prompt`: A string that guides the model on the desired format or content. The maximum length of a prompt is 2,000 tokens.
            - _(Optional)_ `temperature`: A number that controls the randomness of the text. A higher value generates more creative text, while a lower value produces more deterministic text.<br/>

            **Return value**:An object that handles streaming HTTP responses and provides an iterator interface allowing you to process text fragments as they arrive. The maximum length of the response is 4,096 tokens.<br/>
          </Tab>
          <Tab title="Non-streaming responses">
            **Function call**: You call the [`analyze`](/v1.3/sdk-reference/node-js/analyze-videos#open-ended-analysis) method.<br/>

            **Parameters**:
            - `videoId`: The unique identifier of the video for which you want to generate text.
            - `prompt`: A string that guides the model on the desired format or content. The maximum length of a prompt is 2,000 tokens.
            - _(Optional)_ `temperature`: A number that controls the randomness of the text. A higher value generates more creative text, while a lower value produces more deterministic text.<br/>

            **Return value**: An object containing a field named `data` of type `string` representing the generated text. The maximum length of the response is 4,096 tokens.
          </Tab>
        </Tabs>
      </Step>
      <Step title="Process the results">
        <Tabs>
          <Tab title="Streaming responses">
            Use a loop to iterate over the stream. Inside the loop, handle each text fragment as it arrives.
          </Tab>
          <Tab title="Non-streaming responses">
            This example prints the generated text to the standard output.
          </Tab>
        </Tabs>
      </Step>
    </Steps>
  </Tab>
</Tabs>


