from typing import Dict, Any, Optional

# Dictionary of prompt templates for different analysis types
PROMPT_TEMPLATES = {
    "Avaliação de Contrato de Compra e Venda de Imóveis": """
    
       Você é um renomado advogado especialista em direito imobiliário brasileiro, com profundo conhecimento da legislação vigente, da jurisprudência atual e das melhores práticas contratuais do mercado imobiliário nacional.

       Sua missão é realizar uma análise detalhada, crítica e didática do contrato de compra e venda de imóvel apresentado a seguir. A análise deve resultar em um relatório estruturado, que contemple:

       1. **Verificação da conformidade e completude do contrato**  
       Avalie se o contrato contempla todas as cláusulas essenciais e recomendadas, incluindo:  
       - Identificação completa e precisa das partes (nome, CPF, RG, estado civil, endereço e contatos)  
       - Descrição detalhada e alinhada com a matrícula do imóvel (endereço, matrícula, área, confrontações, características físicas)  
       - Valor total, forma de pagamento, prazos, condições para entrada, parcelas, juros, multas e correções monetárias  
       - Prazos e condições para entrega da posse e das chaves  
       - Cláusulas claras sobre rescisão, penalidades e consequências do inadimplemento  
       - Garantias oferecidas pelo vendedor, incluindo inexistência de ônus, dívidas, ações judiciais e responsabilidades por vícios ou defeitos  
       - Responsabilidades quanto a custos, impostos, taxas e despesas de transferência  
       - Procedimentos para formalização, reconhecimento de firma e registro no Cartório de Registro de Imóveis  
       - Due diligence prévia recomendada (verificação de certidões negativas, matrícula atualizada, existência de ônus e ações judiciais)  
       - Cláusulas especiais aplicáveis, como pacto de melhor comprador, retrovenda, venda a contento e direito de preferência (preempção)  
       - Definição do foro para eventuais disputas judiciais  
       - Forma de assinatura (presencial, digital, testemunhas) e segurança jurídica associada  
       - Transparência, clareza e ausência de ambiguidades, evitando brechas que possam gerar litígios futuros  

       2. **Identificação e análise dos riscos**  
       Explique os principais riscos jurídicos e financeiros para:  
       - O comprador (ex.: riscos de ônus ocultos, falta de registro, cláusulas abusivas, prazos não cumpridos)  
       - O vendedor (ex.: inadimplemento, rescisão unilateral, responsabilidade por vícios ocultos)  

       3. **Avaliação dos pontos fortes e pontos fracos**  
       Liste e analise os pontos positivos e negativos do contrato para cada parte, destacando impactos práticos e jurídicos.

       4. **Recomendações e sugestões de melhorias**  
       Proponha ajustes específicos para proteger os interesses de comprador e vendedor, aprimorar a segurança jurídica e mitigar riscos, incluindo sugestões para cláusulas adicionais ou correções textuais.

       5. **Resumo executivo final**  
       Apresente um resumo claro e objetivo das principais conclusões e recomendações para aprimoramento do contrato.

    ---

    ### Instruções adicionais:

    - Baseie sua análise na legislação imobiliária brasileira atualizada, na jurisprudência relevante e nas práticas contratuais consolidadas no mercado.  
    - Utilize linguagem clara, técnica e didática, adequada tanto para profissionais do direito quanto para partes interessadas não especializadas.  
    - Caso o texto fornecido não corresponda a um contrato válido de compra e venda de imóvel, informe explicitamente que o documento não atende aos requisitos legais e formais para tal contrato.  

    ---

    ### Conteúdo para análise:

    {content}

    ---

    ### Estrutura do relatório esperado:

    1. **Resumo do contrato**  
       - Partes envolvidas  
       - Objeto do contrato (descrição detalhada do imóvel)  
       - Finalidade da compra e venda  
       - Principais termos e condições  
       - Datas importantes (assinatura, entrega, rescisão)  
       - Obrigações financeiras (preço, forma de pagamento, multas, juros)  

    2. **Avaliação de riscos**  
       - Riscos para o vendedor  
       - Riscos para o comprador  

    3. **Pontos fortes e pontos fracos**  
       - Pontos fortes para o vendedor  
       - Pontos fortes para o comprador  
       - Pontos fracos para o vendedor  
       - Pontos fracos para o comprador  

    4. **Sugestões de ajustes nas cláusulas**  
       - Recomendações específicas para o vendedor  
       - Recomendações específicas para o comprador  

    5. **Resumo e recomendações finais**

    ---

    Por favor, realize a análise detalhada conforme as instruções acima, assegurando a máxima profundidade, precisão e utilidade prática.

    """,
    
    "Contract Summary": """
    {instructions}
    
    Por favor, forneça um resumo abrangente do seguinte contrato:
    
    {content}
    
    Inclua informações-chave como:
    1. Partes envolvidas
    2. Contract purpose
    3. Key terms and conditions
    4. Important dates (effective date, termination, etc.)
    5. Financial obligations
    6. Notable clauses or provisions
    """,
    
    "Risk Assessment": """
    {instructions}
    
    Please analyze the following contract and identify potential risks:
    
    {content}
    
    Focus on:
    1. Ambiguous language or clauses
    2. Unfavorable terms
    3. Missing protections
    4. Liability concerns
    5. Termination risks
    6. Compliance issues
    
    For each risk identified, please provide:
    - Description of the risk
    - Potential impact
    - Suggested mitigation strategy
    """,
    
    "Legal Compliance Check": """
    {instructions}
    
    Please review the following contract for legal compliance issues:
    
    {content}
    
    Consider:
    1. Jurisdiction-specific requirements
    2. Industry regulations
    3. Standard legal protections
    4. Required disclosures
    5. Enforceability concerns
    6. Recent legal developments that might affect this contract
    
    Provide a compliance assessment with specific references to sections that may need revision.
    """,
    
    "Custom Query": """
    {instructions}
    
    Please analyze the following contract with respect to this specific question:
    
    {custom_query}
    
    Contract:
    {content}
    
    Provide a detailed answer with references to relevant sections of the contract.
    """
}

def format_prompt(
    analysis_type: str,
    content: str,
    custom_query: Optional[str] = None,
    **kwargs
) -> str:
    """
    Format a prompt for the LLM based on the analysis type and content.
    
    Args:
        analysis_type: Type of analysis to perform
        content: The contract content to analyze
        custom_query: Custom question for the "Custom Query" analysis type
        **kwargs: Additional variables to format into the prompt
        
    Returns:
        str: Formatted prompt ready to send to the LLM
    """
    # Get the appropriate template
    template = PROMPT_TEMPLATES.get(
        analysis_type,
        "Please analyze the following contract: {content}"
    )
    
    # Create formatting dictionary with all variables
    format_vars = {
        "content": content,
        "custom_query": custom_query or "",
        **kwargs
    }
    
    # Format the template with the variables
    return template.format(**format_vars)


