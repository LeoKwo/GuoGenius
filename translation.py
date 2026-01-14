def translate(text, languageIsEnglish):
    if languageIsEnglish:
        match text:
            case "more":
                return "💡 Lean more"
            case "info":
                return "💡 GuoGenius is the digital persona of Ruikang Guo. Ask him any question about Ruikang Guo. "
            case "techstack":
                return """
                        #### GuoGenius Tech Stack
                        ```
                        Streamlit
                        LangChain
                        DeepSeek-V3
                        Alibaba Cloud Serverless App Engine (EAS)
                        ```
                        This is an open-source software：[https://github.com/LeoKwo/GuoGenius](https://github.com/LeoKwo/GuoGenius)
                    """
            case "yourquestion":
                return "Your question..."
    else:
        match text:
            case "more":
                return "💡 了解更多"
            case "info":
                return "💡 GuoGenius是郭睿康的数字化分身，拥有关于他的职业经历和技能的一切信息。"
            case "techstack":
                return """
                        #### GuoGenius 技术栈
                        ```
                        Streamlit
                        LangChain
                        DeepSeek-V3
                        阿里云Serverless应用引擎（EAS）
                        ```
                        此项目已开源：[https://github.com/LeoKwo/GuoGenius](https://github.com/LeoKwo/GuoGenius)
                    """
            case "yourquestion":
                return "您的问题 ..."