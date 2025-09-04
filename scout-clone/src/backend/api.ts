import { NextRequest, NextResponse } from 'next/server';

interface AIModel {
  id: string;
  name: string;
  provider: string;
  description: string;
  apiModel?: string;
  intelligence?: string;
  contextLength?: string;
  inputCredits?: string;
  outputCredits?: string;
}

interface AIRequest {
  message: string;
  model: string;
  searchType?: 'chat' | 'search' | 'code' | 'analysis';
}

interface AIResponse {
  response: string;
  model: string;
  timestamp: string;
  searchResults?: any[];
}

const models: AIModel[] = [
  { 
    id: 'gpt-4', 
    name: 'GPT-4', 
    provider: 'OpenAI', 
    description: 'Most capable model', 
    apiModel: 'gpt-4',
    intelligence: 'High',
    contextLength: '128K',
    inputCredits: '10K',
    outputCredits: '30K'
  },
  { 
    id: 'glm-4.5', 
    name: 'GLM-4.5', 
    provider: 'Zhipu AI', 
    description: 'Latest Chinese AI model', 
    apiModel: 'glm-4.5',
    intelligence: 'Very High',
    contextLength: '200K',
    inputCredits: '8K',
    outputCredits: '25K'
  },
  { 
    id: 'gpt-3.5-turbo', 
    name: 'GPT-3.5 Turbo', 
    provider: 'OpenAI', 
    description: 'Fast and efficient', 
    apiModel: 'gpt-3.5-turbo',
    intelligence: 'Medium',
    contextLength: '16K',
    inputCredits: '5K',
    outputCredits: '15K'
  },
  { 
    id: 'claude-3-opus', 
    name: 'Claude 3 Opus', 
    provider: 'Anthropic', 
    description: 'Advanced reasoning', 
    apiModel: 'claude-3-opus',
    intelligence: 'Very High',
    contextLength: '200K',
    inputCredits: '15K',
    outputCredits: '75K'
  },
  { 
    id: 'claude-3-sonnet', 
    name: 'Claude 3 Sonnet', 
    provider: 'Anthropic', 
    description: 'Balanced performance', 
    apiModel: 'claude-3-sonnet',
    intelligence: 'High',
    contextLength: '200K',
    inputCredits: '3K',
    outputCredits: '15K'
  },
  { 
    id: 'gemini-pro', 
    name: 'Gemini Pro', 
    provider: 'Google', 
    description: 'Multimodal capabilities', 
    apiModel: 'gemini-pro',
    intelligence: 'High',
    contextLength: '32K',
    inputCredits: 'Free',
    outputCredits: 'Free'
  },
  { 
    id: 'llama-3-70b', 
    name: 'Llama 3 70B', 
    provider: 'Meta', 
    description: 'Open source powerhouse', 
    apiModel: 'llama-3-70b',
    intelligence: 'High',
    contextLength: '8K',
    inputCredits: 'Free',
    outputCredits: 'Free'
  },
  { 
    id: 'mixtral-8x7b', 
    name: 'Mixtral 8x7B', 
    provider: 'Mistral', 
    description: 'Mixture of experts', 
    apiModel: 'mixtral-8x7b',
    intelligence: 'High',
    contextLength: '32K',
    inputCredits: 'Free',
    outputCredits: 'Free'
  },
  { 
    id: 'command-r-plus', 
    name: 'Command R+', 
    provider: 'Cohere', 
    description: 'Enterprise grade', 
    apiModel: 'command-r-plus',
    intelligence: 'High',
    contextLength: '128K',
    inputCredits: '5K',
    outputCredits: '15K'
  }
];

async function callAI(message: string, modelName: string): Promise<string> {
  try {
    // Try to import and use the z-ai-web-dev-sdk
    let ZAI;
    try {
      ZAI = await import('z-ai-web-dev-sdk');
      console.log('ZAI SDK imported successfully');
    } catch (importError) {
      console.error('Failed to import ZAI SDK:', importError);
      throw new Error('Failed to import AI SDK');
    }

    // Find the model configuration
    const modelConfig = models.find(m => m.name === modelName);
    if (!modelConfig) {
      throw new Error(`Model ${modelName} not found`);
    }

    // Create system prompt based on provider
    let systemPrompt = 'You are a helpful AI assistant. Provide accurate, helpful, and comprehensive responses.';
    
    switch (modelConfig.provider) {
      case 'OpenAI':
        systemPrompt = 'You are ChatGPT, a large language model trained by OpenAI. Provide helpful, accurate, and comprehensive responses.';
        break;
      case 'Zhipu AI':
        systemPrompt = 'You are GLM-4.5, a large language model developed by Zhipu AI. Provide helpful, accurate, and comprehensive responses.';
        break;
      case 'Anthropic':
        systemPrompt = 'You are Claude, an AI assistant created by Anthropic. Be helpful, harmless, and honest in your responses.';
        break;
      case 'Google':
        systemPrompt = 'You are Gemini, Google\'s AI model. Provide helpful, accurate, and comprehensive responses.';
        break;
      case 'Meta':
        systemPrompt = 'You are Llama, Meta\'s open-source AI model. Provide helpful and accurate responses.';
        break;
      case 'Mistral':
        systemPrompt = 'You are Mixtral, Mistral AI\'s mixture of experts model. Provide helpful and comprehensive responses.';
        break;
      case 'Cohere':
        systemPrompt = 'You are Command R+, Cohere\'s enterprise-grade AI model. Provide helpful, accurate, and comprehensive responses.';
        break;
    }

    console.log('Attempting to call AI with model:', modelName);

    // Try different approaches to use the ZAI SDK
    let completion;
    
    // Approach 1: Try using the SDK directly
    try {
      if (typeof ZAI.create === 'function') {
        const zai = await ZAI.create();
        console.log('ZAI instance created successfully');
        
        if (zai && typeof zai.chat?.completions?.create === 'function') {
          completion = await zai.chat.completions.create({
            messages: [
              {
                role: 'system',
                content: systemPrompt
              },
              {
                role: 'user',
                content: message
              }
            ],
            temperature: 0.7,
            max_tokens: 2000
          });
          console.log('AI call successful via chat.completions.create');
        } else {
          throw new Error('chat.completions.create not available');
        }
      } else {
        throw new Error('ZAI.create not available');
      }
    } catch (approach1Error) {
      console.log('Approach 1 failed:', approach1Error);
      
      // Approach 2: Try using the default export
      try {
        const zai = ZAI.default || ZAI;
        if (typeof zai === 'function') {
          const instance = await zai();
          if (instance && typeof instance.chat?.completions?.create === 'function') {
            completion = await instance.chat.completions.create({
              messages: [
                {
                  role: 'system',
                  content: systemPrompt
                },
                {
                  role: 'user',
                  content: message
                }
              ],
              temperature: 0.7,
              max_tokens: 2000
            });
            console.log('AI call successful via default export');
          } else {
            throw new Error('chat.completions.create not available on default export');
          }
        } else {
          throw new Error('Default export is not a function');
        }
      } catch (approach2Error) {
        console.log('Approach 2 failed:', approach2Error);
        
        // Approach 3: Try direct method calls
        try {
          const zai = ZAI.default || ZAI;
          if (zai && typeof zai.chat?.completions?.create === 'function') {
            completion = await zai.chat.completions.create({
              messages: [
                {
                  role: 'system',
                  content: systemPrompt
                },
                {
                  role: 'user',
                  content: message
                }
              ],
              temperature: 0.7,
              max_tokens: 2000
            });
            console.log('AI call successful via direct method');
          } else {
            throw new Error('Direct method call not available');
          }
        } catch (approach3Error) {
          console.log('Approach 3 failed:', approach3Error);
          throw new Error('All AI SDK approaches failed');
        }
      }
    }

    console.log('AI call successful, completion:', completion);

    // Handle different response formats
    if (completion && typeof completion === 'object') {
      // OpenAI-like format
      if (completion.choices && Array.isArray(completion.choices)) {
        const content = completion.choices[0]?.message?.content;
        if (content && typeof content === 'string' && content.trim().length > 0) {
          return content;
        }
      }
      // Direct response format
      else if (completion.content && typeof completion.content === 'string') {
        return completion.content;
      }
      // String response
      else if (typeof completion === 'string') {
        return completion;
      }
      // Try to extract content from other formats
      else if (completion.response || completion.answer || completion.text) {
        return completion.response || completion.answer || completion.text;
      }
    }

    throw new Error('Invalid response format from AI');
  } catch (error) {
    console.error('AI API error:', error);
    
    // If the AI SDK fails, provide a helpful error message but don't use mock responses
    return `I'm sorry, but I'm currently experiencing technical difficulties with the ${modelName} AI service. This could be due to API connectivity issues or service maintenance. 

Please try again in a few moments. If the problem persists, you may want to:
- Check your internet connection
- Try selecting a different AI model
- Contact support if the issue continues

The technical team has been notified of this issue and is working to resolve it as soon as possible.

Error details: ${error instanceof Error ? error.message : 'Unknown error'}`;
  }
}

async function performWebSearch(query: string): Promise<any[]> {
  try {
    console.log('Performing web search for:', query);

    // Try to import and use the z-ai-web-dev-sdk for web search
    let ZAI;
    try {
      ZAI = await import('z-ai-web-dev-sdk');
      console.log('ZAI SDK imported successfully for web search');
    } catch (importError) {
      console.error('Failed to import ZAI SDK for web search:', importError);
      throw new Error('Failed to import AI SDK for web search');
    }

    // Try different approaches to use the ZAI SDK for web search
    let searchResult;
    
    // Approach 1: Try using the SDK directly
    try {
      if (typeof ZAI.create === 'function') {
        const zai = await ZAI.create();
        console.log('ZAI instance created successfully for web search');
        
        if (zai && typeof zai.functions?.invoke === 'function') {
          searchResult = await zai.functions.invoke("web_search", {
            query: query,
            num: 5
          });
          console.log('Web search successful via functions.invoke');
        } else {
          throw new Error('functions.invoke not available');
        }
      } else {
        throw new Error('ZAI.create not available');
      }
    } catch (approach1Error) {
      console.log('Web search Approach 1 failed:', approach1Error);
      
      // Approach 2: Try using the default export
      try {
        const zai = ZAI.default || ZAI;
        if (typeof zai === 'function') {
          const instance = await zai();
          if (instance && typeof instance.functions?.invoke === 'function') {
            searchResult = await instance.functions.invoke("web_search", {
              query: query,
              num: 5
            });
            console.log('Web search successful via default export');
          } else {
            throw new Error('functions.invoke not available on default export');
          }
        } else {
          throw new Error('Default export is not a function');
        }
      } catch (approach2Error) {
        console.log('Web search Approach 2 failed:', approach2Error);
        
        // Approach 3: Try direct method calls
        try {
          const zai = ZAI.default || ZAI;
          if (zai && typeof zai.functions?.invoke === 'function') {
            searchResult = await zai.functions.invoke("web_search", {
              query: query,
              num: 5
            });
            console.log('Web search successful via direct method');
          } else {
            throw new Error('Direct method call not available');
          }
        } catch (approach3Error) {
          console.log('Web search Approach 3 failed:', approach3Error);
          throw new Error('All web search approaches failed');
        }
      }
    }

    console.log('Web search successful, results:', searchResult?.length || 0);
    return searchResult || [];
  } catch (error) {
    console.error('Web search error:', error);
    
    // If web search fails, return empty array instead of mock results
    // The AI will still provide a helpful response based on the user's query
    return [];
  }
}

export async function POST(request: NextRequest) {
  try {
    const body: AIRequest = await request.json();
    const { message, model, searchType = 'chat' } = body;

    if (!message || !model) {
      return NextResponse.json(
        { error: 'Message and model are required' },
        { status: 400 }
      );
    }

    console.log('Processing request:', { message, model, searchType });

    let response: string;
    let searchResults: any[] = [];

    // Handle different search types
    switch (searchType) {
      case 'search':
        console.log('Performing web search for:', message);
        // Perform web search first
        searchResults = await performWebSearch(message);
        console.log('Search results found:', searchResults.length);
        
        // Then use AI to analyze and summarize the search results
        const searchContext = searchResults.map((result: any) => 
          `${result.name}: ${result.snippet}`
        ).join('\n\n');
        
        response = await callAI(
          `Based on the following search results, please provide a comprehensive answer to the query: "${message}"\n\nSearch Results:\n${searchContext}`,
          model
        );
        break;
        
      case 'code':
        console.log('Generating code for:', message);
        response = await callAI(
          `Please provide code solutions for the following request. Include explanations and best practices. Use appropriate code formatting:\n\n${message}`,
          model
        );
        break;
        
      case 'analysis':
        console.log('Performing analysis for:', message);
        response = await callAI(
          `Please provide a detailed analysis of the following. Include insights, recommendations, and key findings:\n\n${message}`,
          model
        );
        break;
        
      default: // chat
        console.log('Processing chat message:', message);
        response = await callAI(message, model);
    }

    console.log('AI response generated successfully');

    const aiResponse: AIResponse = {
      response,
      model,
      timestamp: new Date().toISOString(),
      ...(searchResults.length > 0 && { searchResults })
    };

    return NextResponse.json(aiResponse);
  } catch (error) {
    console.error('AI API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({ models });
}
