from typing import Dict, Any, Optional

# Dictionary of prompt templates for different analysis types
PROMPT_TEMPLATES = {
    "Avaliação de Contrato de Compra e Venda de Imóveis": """
       
       {instructions}

       Você é um especialista em direito imobiliário brasileiro e legislação vigente. 
       Realize uma análise detalhada do seguinte contrato de compra e venda de imóvel, considerando as boas práticas do direito imobiliário brasileiro e a legislação vigente.
       O resultado da sua avaliação será utilizado para esclarecer dúvidas e fornecer recomendações práticas para compradores e vendedores no contrato. Seja didático.

       As boas práticas em contratos de compra e venda de imóveis e os itens essenciais do direito imobiliário e contratual que devem ser respeitados incluem os seguintes pontos fundamentais:

       1. Identificação completa das partes
       O contrato deve conter os dados pessoais completos do comprador e do vendedor, como nome, CPF, RG, estado civil, endereço e, se possível, contatos atualizados. Essa qualificação é essencial para evitar dúvidas futuras e garantir segurança jurídica.
       2. Descrição detalhada do imóvel
       É imprescindível descrever com precisão o imóvel objeto da venda, incluindo endereço, número da matrícula no Cartório de Registro de Imóveis, área construída, área total do terreno, características específicas e limites. A descrição deve estar alinhada com a matrícula para evitar conflitos.
       3. Preço e condições de pagamento
       O contrato deve estipular claramente o valor total da negociação, detalhar se haverá entrada, o número de parcelas, datas de vencimento, forma de pagamento (à vista, financiamento, etc.) e incluir taxas e juros, se houver. Também é importante prever cláusulas que tratem do inadimplemento, como multas e juros de mora.
       4. Prazos e condições para entrega do imóvel
       Definir a data e as condições para a entrega das chaves e posse do imóvel é fundamental para evitar conflitos posteriores entre as partes.
       5. Cláusulas de rescisão e penalidades
       O contrato deve prever o que acontece em caso de cancelamento, inadimplência ou descumprimento de qualquer cláusula, estabelecendo penalidades claras para garantir o cumprimento do acordo.
       6. Garantias e responsabilidades
       É necessário estipular as garantias oferecidas pelo vendedor, como a inexistência de ônus, dívidas ou ações judiciais sobre o imóvel, e as responsabilidades das partes quanto a possíveis vícios ou defeitos do imóvel.
       7. Formalização e registro
       Após a assinatura, o contrato deve ser levado ao cartório para reconhecimento de firma, o que confere maior segurança jurídica. A escritura pública deve ser lavrada em Cartório de Notas, especialmente em casos de imóveis de alto valor ou financiados, e o registro da escritura no Cartório de Registro de Imóveis é o ato que torna o comprador o proprietário legal do imóvel.
       8. Due diligence prévia
       Antes da formalização, é essencial realizar uma análise completa da documentação do imóvel, verificando certidões negativas, matrícula atualizada, existência de ônus reais e ações judiciais, para evitar fraudes e garantir a segurança da transação.
       9. Cláusulas especiais (quando aplicáveis)
       Podem ser incluídas cláusulas específicas como pacto de melhor comprador, retrovenda, venda a contento (condição suspensiva) e preempção (direito de preferência), que devem estar claras e, quando necessário, registradas na matrícula do imóvel.
       10. Transparência e clareza
       Todo o contrato deve ser redigido de forma clara, completa e sem brechas, evitando termos ambíguos que possam gerar interpretações equivocadas ou litígios futuros. O ideal é contar com o auxílio de um advogado especializado para elaboração e revisão do contrato

       {content}
       
       Inclua as seguintes informações chaves seções:

       1. Resumo do contrato:
          - Partes envolvidas
          - Objeto do contrato (descrição do imóvel)
          - Finalidade da compra e venda
          - Principais termos e condições
          - Datas importantes (data de assinatura, prazo para entrega, rescisão, etc.)
          - Obrigações financeiras (preço, forma de pagamento, multas, etc.)

       2. Avaliação de riscos:
          - Identifique e explique os principais riscos para o vendedor
          - Identifique e explique os principais riscos para o comprador

       3. Pontos fortes e pontos fracos:
          - Liste e analise os pontos fortes para o vendedor
          - Liste e analise os pontos fortes para o comprador
          - Liste e analise os pontos fracos para o vendedor
          - Liste e analise os pontos fracos para o comprador

       4. Sugestões de ajustes nas cláusulas:
          - Recomendações específicas para proteger os interesses do vendedor
          - Recomendações específicas para proteger os interesses do comprador

       5. Resumo da anáilse e recomendações de melhoria do texto do contrato.

       Analise com base na legislação imobiliária brasileira, jurisprudência e práticas contratuais comuns no mercado imobiliário do Brasil.
 
       Se o texto não for de um contrato de copra e venda de imóvel, forneça uma mensagem explicando que o texto não atende aos requisitos do contrato de compra e venda de imóveis.
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


