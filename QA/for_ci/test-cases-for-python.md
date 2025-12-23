# Python SDK gen failing on relative tsp path

## question
This is my 1st time trying to create our Python SDK. The pipeline appears to be failing due to relative paths for included tsp files. Any idea how to get around this?

```
Errors occurred while generating SDK from specification/discoverydev/Discovery.Workspace/tspconfig.yaml. Follow the steps at https://aka.ms/azsdk/sdk-automation-faq#how-to-view-the-detailed-sdk-generation-errors to view detailed errors.
2025-10-08 16:27:29 [ERROR] ====== Error occurred in tsp compiler (error stack start) ======
2025-10-08 16:27:29 [ERROR] /mnt/vss/_work/1/s/azure-sdk-for-python-pr/sdk/discovery-workspace/azure-discovery-workspace/TempTypeSpecFiles/Discovery.Workspace/common.tsp:1:1 - error import-not-found: Couldn't resolve import "../Discovery.Shared/namespace.tsp"
2025-10-08 16:27:29 [ERROR] /mnt/vss/_work/1/s/azure-sdk-for-python-pr/sdk/discovery-workspace/azure-discovery-workspace/TempTypeSpecFiles/Discovery.Workspace/common.tsp:3:1 - error import-not-found: Couldn't resolve import "../Discovery.Shared/data-plane.tsp"
2025-10-08 16:27:29 [ERROR] /mnt/vss/_work/1/s/azure-sdk-for-python-pr/sdk/discovery-workspace/azure-discovery-workspace/TempTypeSpecFiles/Discovery.Workspace/common.tsp:4:1 - error import-not-found: Couldn't resolve import "../Discovery.Shared/shared.tsp"
2025-10-08 16:27:29 [ERROR] /mnt/vss/_work/1/s/azure-sdk-for-python-pr/sdk/discovery-workspace/azure-discovery-workspace/TempTypeSpecFiles/Discovery.Workspace/_project.tsp:5:1 - error import-not-found: Couldn't resolve import "../Discovery.Shared/data-plane.tsp"
2025-10-08 16:27:29 [ERROR] /mnt/vss/_work/1/s/azure-sdk-for-python-pr/sdk/discovery-workspace/azure-discovery-workspace/TempTypeSpecFiles/Discovery.Workspace/_conversation_message_logs.tsp:6:1 - error import-not-found: Couldn't resolve import "../Discovery.Shared/data-plane.tsp"
2025-10-08 16:27:29 [ERROR] /mnt/vss/_work/1/s/azure-sdk-for-python-pr/sdk/discovery-workspace/azure-discovery-workspace/TempTypeSpecFiles/Discovery.Workspace/_tool.tsp:5:1 - error import-not-found: Couldn't resolve import "../Discovery.Shared/data-plane.tsp"
2025-10-08 16:27:29 [ERROR] /mnt/vss/_work/1/s/azure-sdk-for-python-pr/sdk/discovery-workspace/azure-discovery-workspace/TempTypeSpecFiles/Discovery.Workspace/_tool.tsp:6:1 - error import-not-found: Couldn't resolve import "../Discovery.Shared/shared.tsp"
```

## answer
According to error log, it seems that your typespec refer to folder outside project folder but you don't declare it in `tspconfig.yaml`. You could add the missing dir like below then try again:
```
"@azure-tools/typespec-client-generator-cli":
  additionalDirectories:
    - "specification/keyvault/Security.KeyVault.Common/"
```

# MS Learning Documentation Categorization as "Unknown"

## question
I've released the preview version of azure-ai-transcription (v1.0.0b1), but the documentation is appearing under the "unknown" folder on Microsoft Learn instead of the cognitive-services category.

During the documentation build, the warning shows:
```
##[warning]Could not retrieve metadata for azure-ai-transcription from metadata CSV. Using best effort defaults.
The service of package: cognitiveservices
```

Can someone help take a look of this issue? Does it require register this package in the metadata CSV with MSDocService: cognitive-services so the documentation appears in the correct location on Microsoft Learn?

Here is the release [pipeline link: Pipelines - Run 20251203.2](https://dev.azure.com/azure-sdk/internal/_build/results?buildId=5633753&view=results)
Here is MS learning link: [Azure AI Speech Transcription client library for Python | Microsoft Learn](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-transcription-readme?view=azure-python-preview)

## answer
Yes, to ensure the documentation for azure-ai-transcription appears under the "cognitive-services" category on Microsoft Learn, you need to add or update the metadata for this package in the metadata CSV file located at https://github.com/Azure/azure-sdk/blob/main/_data/releases/latest/python-packages.csv.
Specifically, you should:
1. Find (or add) the row for azure-ai-transcription in python-packages.csv.
2. Set the MSDocService field to "cognitive-services". This value is used to correctly categorize the package in the Learn docs hierarchy.
3. Ensure other relevant fields (ServiceName, DisplayName, Type, etc.) are filled in appropriately.
After updating the CSV, commit and create a PR in the azure-sdk repo. Once merged, the next docs build will pick up the new metadata and your package will be categorized correctly.
If the Notes field for your package is set to "Needs Review", update it to another value to avoid automation overwriting your changes.
References and field details can be found here:
- [CSV field README](https://github.com/Azure/azure-sdk/blob/main/eng/README.md#csv-fields)
- [Relevant CSV file for Python packages](https://github.com/Azure/azure-sdk/blob/main/_data/releases/latest/python-packages.csv)
In summary: Yes, registering your package in the metadata CSV with MSDocService: cognitive-services is required. This action will resolve the warning and correct the Learn categorization.
**References**
[Publish SDK reference docs / Onboard a released package | Azure-sdk-docs-eng](https://eng.ms/docs/products/azure-developer-experience/develop/sdk-docs)
[Metadata CSV update process for Python | Azure Sdk For Python Docs](https://github.com/Azure/azure-sdk-for-python/blob/main/doc/deprecation_process.md)

# "black" job in pipeline fails, but when I run locally, the tool does not make any changes

## question
I like to run the "black" tool before PRs, and I ask others in my project to do the same. A few hours ago I found out that I can turn on this check in the pipeline. I was happy to see this. So I added the following to pyproject.toml:

```
[tool.azure-sdk-build]
black = true
```

I run "black" before commiting my last change to the PR, and no updates were needed.

But the pipeline called out a "black" failure: https://dev.azure.com/azure-sdk/public/_build/results?buildId=5606772&view=logs&j=b70e5e73-bbb6-5567-0939-8415943fadb9&t=efe9ac6d-3fdb-50af-24e1-4319f36eecb4

I see the pipeline used black version 24.4.0. I had a newer version when I run locally. I install 24.4.0 and run that, but it also did not do any changes to the code.

Any idea how to fix it? (other than removing it from the pipeline...).

## answer
The "black" job in the Azure SDK for Python pipeline can fail for reasons beyond just code formatting. Even if running "black" locally with the same version (24.4.0) does not produce changes, there are a few areas to check for a root cause:
1. Run Black with the Same Arguments as the Pipeline:The pipeline runs "black" using tox with specific arguments. Make sure you are running locally in the same way. From the official guidance, run: `tox run -e black -c ../../../eng/tox/tox.ini --root . -- .` This ensures that the same config files, paths, and excludes are used. The pipeline may use a different configuration or target files that you are not formatting locally. Or you can tried the same command used by ci: `python -m azpysdk.main black --isolate sdk/ai/azure-ai-projects`.
2. Check for Hidden Files or Config Differences: The pipeline uses the repository’s configuration, including pyproject.toml and any exclude/include patterns. Local runs may inadvertently skip files due to local ignore files, environment differences, or working directory mismatches. Double-check that your local environment matches the CI context.
3. Run `git status` or `git diff` to find out whether there are files already formatted but not pushed to the pr.
4. Line Endings and Whitespace: Sometimes, black fails due to line ending differences (CRLF vs LF) or invisible whitespace issues that are not flagged locally. Make sure your files have consistent line endings (prefer LF in repo).
5. Check the Pipeline Log for Specific Files: Review the pipeline's failure log closely to see which files are reported as needing formatting. Sometimes, it’s a file outside your typical working set (such as generated code or test files).
6. Reproduce in a Clean Environment: To eliminate local state issues, clone your repo in a fresh directory and re-run the pipeline’s black command as above. If you confirm that running "black" via tox in a clean environment with the same version does not report changes, but the pipeline still fails, check for possible pipeline caching or artifact issues. Otherwise, use the pipeline log to identify exactly which file is causing the failure and focus on that file. Removing the check is not recommended; instead, focus on aligning your local runs with the pipeline invocation. If you continue to see unexplained failures, reach out in the Azure SDK language team channel with your findings and the specific pipeline log excerpt.

# Ubunty 2303 pypy39 specific failure

## question
Hi,

I am seeing this error in the pipeline. Can anyone check please?
```
         --- stderr
        error: the configured PyPy interpreter version (3.9) is lower than
      PyO3's minimum supported version (3.11)
      warning: build failed, waiting for other jobs to finish...
```
[Pipelines - Run 20251030.12 logs](https://dev.azure.com/azure-sdk/public/_build/results?buildId=5517166&view=logs&j=98792cce-2755-554b-a8ad-f8c76be41d33&t=7feb2094-2399-5589-4545-1b2ca3b7ddc8)

## answer
You have a dependency that doesn't ship a pypy39 dep. That's all. You could swap that with pypy311 in your matrix if you wanted to give it a shot.

# Python emitter issue with bulleted list TypeSpec doc string, and other

## question
This TypeSpec repo/branch/folder: https://github.com/Azure/azure-rest-api-specs-pr/tree/feature/ai-foundry/agents-v2/specification/ai/Azure.AI.Projects

Is emitted into this Python repo/branch/folder: https://github.com/Azure/azure-sdk-for-python/tree/feature/azure-ai-projects/2.0.0b1/sdk/ai/azure-ai-projects

Using the command `tsp-client update --debug --local-spec-repo <path>`

I have a green build, other than errors in the "Build Docs" stage, as seen in this build of the branc: https://dev.azure.com/azure-sdk/internal/_build/results?buildId=5527867&view=results

I need some guidance on how to update TypeSpec to make these Python doc generation go away.

The errors are the following:
```
updating environment: [new config] 7 added, 0 changed, 0 removed
docstring of azure.ai.projects.models.Reasoning.generate_summary:6: WARNING: Inline strong start-string without end-string. [docutils]
docstring of azure.ai.projects.models.WorkflowDefinition.workflow:2: WARNING: Duplicate explicit target name: "learn more". [docutils]
docstring of azure.ai.projects.models.WorkflowDefinition.workflow:2: WARNING: Duplicate explicit target name: "learn more". [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:54: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:61: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:64: ERROR: Unexpected indentation. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:65: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:67: ERROR: Unexpected indentation. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:79: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:82: ERROR: Unexpected indentation. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:83: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:89: ERROR: Unexpected indentation. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:90: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:109: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._models.Response:112: ERROR: Unexpected indentation. [docutils]
docstring of azure.ai.projects.models.WorkflowDefinition.workflow:2: WARNING: Duplicate explicit target name: "learn more". [docutils]
docstring of azure.ai.projects.models.Response.output:10: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
docstring of azure.ai.projects.models.Response.output:12: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
docstring of azure.ai.projects.models.Response.tools:9: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
docstring of azure.ai.projects.models.Response.tools:12: ERROR: Unexpected indentation. [docutils]
docstring of azure.ai.projects.models.Response.tools:13: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
docstring of azure.ai.projects.models.Response.truncation:8: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
docstring of azure.ai.projects.models.Response.truncation:11: ERROR: Unexpected indentation. [docutils]
docstring of azure.ai.projects.models.Response.truncation:12: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
docstring of azure.ai.projects.models.WorkflowDefinition.workflow:2: WARNING: Duplicate explicit target name: "learn more". [docutils]
E:\src\sdk-repos\azure-sdk-for-python\sdk\ai\azure-ai-projects\.tox\sphinx\Lib\site-packages\azure\ai\projects\models\__init__.py:docstring of azure.ai.projects.models._enums.ServiceTier:4: WARNING: Bullet list ends without a blank line; unexpected unindent. [docutils]
```

It comes from two TypeSpec models, direct link here:
Response model - https://github.com/Azure/azure-rest-api-specs-pr/blob/feature/ai-foundry/agents-v2/specification/ai/Azure.AI.Projects/.external-readonly/openai.external.typespec/responses/custom.tsp#L38
```
model Response {
  ...Response_Pre_Update;
  conversation: {
    id: string;
  } | null;
}
```
ServiceTier union - https://github.com/Azure/azure-rest-api-specs-pr/blob/feature/ai-foundry/agents-v2/specification/ai/Azure.AI.Projects/.external-readonly/openai.external.typespec/common/models.tsp#L475
```
union ServiceTier {
  "auto",
  "default",
  "flex",
  "scale",
  "priority",
}
```

## answer
The Sphinx docstring errors you're seeing in the generated Python SDK (unexpected indentation, block quote ends without a blank line, duplicate explicit target names, bullet/definition list issues) are caused by how TypeSpec documentation comments are emitted into Python docstrings, especially when those comments use Markdown or formatting that doesn't map cleanly to reStructuredText (reST), which Sphinx expects.
To resolve these errors, there are two possible solutions:
1. You need to ensure that the TypeSpec doc comments for the Response model and ServiceTier union are written in a way that avoids problematic Markdown constructs and closely follows what Sphinx/reST expects.
Here are practical steps:
- **Bullet/Definition List Formatting:** - Avoid using Markdown bullet lists (`*`, `-`, or `+`) or definition lists in your TypeSpec doc comments. Instead, use plain sentences, or, if you need a list, format it as numbered items with clear line breaks between each item. - If you must use a list, add a blank line before and after the list, and ensure each item starts on a new line. Do not nest lists or use complex indentation.
- **Inline Strong/Emphasis Markup:** - If you use `**bold**` or `*italic*` in TypeSpec comments, Sphinx may misinterpret these if not balanced. Prefer using plain text or ensure that every start marker has a matching end marker.
- **Explicit Targets (Links):** - If you use `[Learn more](url)` in doc comments, emitting these into Python docstrings can result in duplicate explicit target names. Use plain URLs or avoid repeating the same anchor text multiple times.
- **Block Quotes:** - Avoid using Markdown block quotes (`>`) in TypeSpec doc comments. If you need to highlight something, use plain sentences.
- **Unexpected Indentation:** - Ensure all TypeSpec doc comments are left-aligned, with no leading spaces or tabs before the text, unless you are deliberately creating a code block. For code blocks, use triple backticks and add blank lines before and after the block.
- **General Style:** - Write documentation in simple paragraphs. Do not mix Markdown with reST, and avoid complex formatting. - Example of a safe docstring for a model property: ```tsp /** * The list of available service tiers. Possible values include: * 1. Basic - Entry-level tier. * 2. Standard - Recommended for most workloads. * 3. Premium - Advanced tier for high throughput. */ ``` - Avoid: ```tsp /** * - Basic * - Standard * - Premium */ ``` **Actionable Steps:** - Go to your TypeSpec definitions for Response and ServiceTier, and revise any doc comments containing bullet lists, definition lists, block quotes, repeated anchor text, or excessive indentation. Replace with simple sentences or numbered lists as above. - After making these changes, regenerate the Python SDK and run the Sphinx build again. The warnings/errors should be resolved. - For reference on Python docstring formatting and Sphinx compatibility, see the Azure Python SDK [docstring guidelines](https://github.com/Azure/azure-sdk-for-python/blob/main/doc/dev/docstring.md). If you need a specific example for ServiceTier: ```tsp /** * Service tier for deployment. Possible values: * 1. Basic: Entry-level tier. * 2. Standard: Recommended tier. * 3. Premium: Advanced tier for large workloads. */ union ServiceTier { ... } ``` And for Response model, ensure any lists or references are in plain sentences and do not use block quotes or repeated links.
2. Or you can disable the sphinx environment within the pyproject.toml for the problematic package. By that way you won't hit these sphinx failures.
```
[tool.azure-sdk-build]
sphinx = false
```
