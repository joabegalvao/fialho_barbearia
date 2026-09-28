# Fialho Barbearia | Landing page

Página única, estática, em HTML, CSS e JavaScript puro. Não há etapa de build
nem dependências de execução: basta servir a pasta.

## Como visualizar

```bash
# na raiz do projeto
python3 -m http.server 4174
# abra http://localhost:4174
```

Qualquer servidor estático funciona (Nginx, Apache, Netlify, Vercel, Hostinger).
Publique `index.html` e a pasta `assets/`. A pasta `tools/` não precisa ir para
o servidor.

### Materiais de origem

Os arquivos enviados pelo cliente (`fialho_barbearia.jpg`, `Screenshot *.png`,
`Richard_Derner.png`, `Ronny_Matheus.png`, `Jose_Gerdes.png` e `dados.txt`) não
fazem parte do repositório. Eles ficam na raiz da pasta local do projeto e são
ignorados pelo git. As imagens que o site usa já estão prontas em `assets/img`.

Só é preciso ter os originais para rodar `tools/optimize-images.py`, ou seja,
para trocar ou reprocessar uma foto.

## Estratégia

| Definição | Decisão |
| --- | --- |
| Proposta de valor | Corte e barba feitos sem pressa, com hora marcada pela agenda online, num salão onde dá vontade de ficar |
| Principal objeção | "Vou conseguir horário e sair com o corte do jeito que pedi? E a assinatura compensa?" |
| Conversão prioritária | Agendar horário na agenda online (AppBarber) |
| Ação secundária | Conhecer os planos do Clube Fialho |
| Ações de apoio | Chamar no WhatsApp e seguir o Instagram @fialhobarbearia_ |

## Seções da página

| Ordem | Seção | Âncora | Conteúdo |
| --- | --- | --- | --- |
| 1 | Cabeçalho | | Logo, navegação e CTA de agendamento. Fixo no topo |
| 2 | Hero | `#inicio` | Proposta de valor, CTA principal e três fatos (endereço, agenda, Clube) |
| 3 | A casa | `#a-casa` | O salão em duas fotos e quatro detalhes do ambiente |
| 4 | Serviços | `#servicos` | Cabelo, barba e produtos, com link para a agenda |
| 5 | Avaliações | `#avaliacoes` | Três depoimentos de clientes, um em destaque |
| 6 | Clube Fialho | `#clube` | Plano de assinatura e link para a página de planos |
| 7 | Como agendar e onde fica | `#onde-fica` | Três passos, endereço, mapa, WhatsApp e telefone |
| 8 | Chamada final | | Agenda e Instagram |
| 9 | Rodapé | | Contato, atendimento e redes sociais |

Componentes de apoio:

- Botão flutuante de WhatsApp, no canto inferior direito, em todas as telas.
- Barra fixa com o CTA de agendamento no celular. Ela aparece depois do hero e
  some onde a página já tem um botão de ação próprio. Quando a barra está
  visível, o botão de WhatsApp sobe para não cobri-la.

## Estrutura de arquivos

```
index.html                 conteúdo e SEO
assets/css/styles.css      estilos (tokens de cor e tipografia no topo)
assets/js/main.js          menu, revelação na rolagem, barra fixa no celular
assets/img/                imagens otimizadas (geradas pelo script)
assets/fonts/              Archivo e Instrument Serif (arquivos locais)
tools/optimize-images.py   gera assets/img a partir dos originais
```

## Como atualizar o conteúdo

| O que mudar | Onde |
| --- | --- |
| Textos, endereço, telefone | `index.html` (seções comentadas) |
| Link da agenda | `index.html`: procure por `sites.appbarber.com.br/fialhobarbearia-07zd` (7 ocorrências) |
| Link do Clube Fialho | `index.html`: procure por `appbarber.com.br/assinar` (2 ocorrências) |
| Telefone | `index.html`: seção "Onde fica", rodapé e bloco JSON-LD no `<head>` |
| Número e mensagem do WhatsApp | `index.html`: procure por `wa.me/` (3 ocorrências). O texto vem depois de `?text=`, com espaços escritos como `%20` e acentos codificados |
| Cores e fontes | `assets/css/styles.css`, bloco `:root` |
| Fotos | substitua o original, ajuste a lista `PHOTOS` em `tools/optimize-images.py` e rode o script |
| Foto com faixa na borda | acrescente o arquivo à lista `CROPS` do script (esquerda, topo, direita, base, em pixels) e rode o script |
| Avaliações | `index.html`, seção "AVALIAÇÕES". Fotos de perfil: lista `AVATARS` do script |
| Novo serviço | copie um bloco `<li class="service">` e ajuste o número |

Para gerar as imagens (requer Pillow e os materiais de origem na raiz do
projeto):

```bash
python3 tools/optimize-images.py
```

Se a proporção de uma foto mudar, atualize `width` e `height` da tag `<img>`
correspondente no `index.html`, para não haver salto de layout.

### Título do hero

O título tem três linhas fixas, e o tamanho da letra é calculado para que a
linha mais larga caiba na coluna em qualquer tela. Se o texto mudar, confira a
quebra em 320 px e em 760 px de largura. A regra está em `.hero__title`, no
`styles.css`.

### Cache do navegador

Os arquivos de estilo e script são chamados com versão: `styles.css?v=2` e
`main.js?v=2`. Ao alterar um deles, aumente o número no `index.html` para que
os visitantes recebam a versão nova.

## Identidade visual

| Token | Cor | Origem |
| --- | --- | --- |
| `--ink` | `#0D0C0D` | fundo do logo |
| `--ivory` | `#E2DED1` | letras do logo |
| `--copper` | `#C48D63` | filetes e ornamentos do logo |
| `--copper-700` | `#85502C` | cobre escurecido, para texto sobre fundo claro |
| `--ink-800`, `--ink-700`, `--ink-line` | `#171514`, `#221F1D`, `#38322D` | superfícies e linhas sobre o fundo escuro |
| `--paper`, `--sand`, `--line` | `#F3EFE6`, `#E3DCCD`, `#CBC1AE` | neutros tirados da toalha e da parede de concreto das fotos |
| `--whatsapp` | `#25D366` | verde oficial do WhatsApp, usado só no botão flutuante |

Tipografia: Archivo (títulos em versão condensada e caixa alta, textos em
largura normal) e Instrument Serif itálica (destaques). É um único arquivo
variável de Archivo para os dois usos.

Elementos que vêm da marca e do salão:

- Títulos condensados em caixa alta, como letreiro de fachada, com uma linha em
  serifa itálica que retoma o floreio do logo.
- Ponto antes dos rótulos de seção, como os que ladeiam "BARBEARIA" no logo.
- Anéis ao redor do selo na seção do Clube, que ampliam os círculos
  concêntricos do logo.
- Faixa listrada abaixo do hero, referência ao poste de barbeiro que aparece
  nas fotos.

O fundo escuro da página usa exatamente a cor de fundo do logo, para que o
selo se integre sem recorte visível.

### Tratamento do logo

O arquivo recebido (`fialho_barbearia.jpg`) tem 447 x 447 px. Nada foi
redesenhado. O script limpa o ruído de compressão do fundo, que passa a ter a
cor exata `#0D0C0D`, e torna transparente a área fora do círculo.

### Tratamento das fotos

As fotos recebidas são capturas de tela com cerca de 665 px de largura. O
script remove 2 px de cada borda e gera versões menores. Nenhuma foto é
ampliada, e o layout nunca as exibe acima de 440 px de largura.

## Decisões de conteúdo

- Só foram usados dados fornecidos: nome, segmento, endereço, telefone, links,
  redes sociais, fotos e avaliações. Não há métricas, prêmios, preços ou
  promessas inventadas.
- Os detalhes do salão (poltronas, sofá, geladeira, ar-condicionado, tapete,
  poste de barbeiro) e a toalha quente foram descritos a partir das fotos.
- "Marca própria" foi entendida como a marca Fialho, não como uma linha de
  produtos. A página cita produtos para cabelo e barba sem nomear nenhum.
- O botão flutuante e os links de WhatsApp usam o número (44) 99809-2162, o
  único informado, com a mensagem "Olá! Vi o site da Fialho Barbearia e quero
  agendar um horário." já preenchida. O mesmo número também aparece como link
  de ligação (`tel:`).
- O ícone do botão flutuante é escuro sobre o verde, e não branco, para manter
  contraste suficiente.
- Avaliações: as palavras são as enviadas pelo cliente. No depoimento de José
  Gerdes foram corrigidos três erros de digitação ("é o corte Excelente" para
  "e o corte excelente", "Ja" para "Já") e acrescentado o ponto final. Os
  outros dois estão como recebidos.
- Avaliações sem estrelas e sem citação de fonte, porque nota e origem não
  foram informadas.
- A seção do Clube Fialho não cita preço, frequência nem benefícios, porque
  esses dados não foram fornecidos. Ela leva à página de assinatura.
- Não há formulário, porque não existe destino de envio definido.
- Não há seção de perguntas frequentes, por falta de dados sobre horários,
  formas de pagamento e política de cancelamento.
- O link do Facebook foi publicado sem o parâmetro de rastreamento `mibextid`.

## Testes realizados

Executados em 28/09/2026, em Chromium automatizado (Playwright).

- Revisão visual das capturas de tela: página inteira em 390 e 1440 px,
  primeira dobra em 320, 768 e 1024 px.
- Sem rolagem horizontal e com o título do hero em três linhas nos tamanhos
  320, 360, 390, 600, 768, 820, 900, 1024, 1200, 1366, 1440 e 1920 px.
- Sem erros de console e sem imagens quebradas.
- 50 verificações automáticas aprovadas: menu no celular (toque, Esc, toque
  fora, foco), âncoras, barra fixa, botão flutuante de WhatsApp (posição,
  mensagem preenchida, sem cobrir a barra fixa nem o rodapé), revelação na
  rolagem, link de pular para o conteúdo, foco visível, destino e atributos de
  todos os links, hierarquia de títulos e atributos das imagens.
- Página utilizável sem JavaScript.
- Animações desligadas quando o sistema pede movimento reduzido.
- Contraste AA em todos os textos (mínimo de 4,84:1).
- Carga inicial no celular de 403 KB, sem saltos de layout (CLS 0).

Não testado: Safari, Firefox e aparelhos físicos. Dos links externos, foi
conferido apenas o endereço, não o conteúdo de destino. Isso inclui o
WhatsApp: não foi verificado se o número responde. A página da agenda no
AppBarber tem verificação contra acesso automatizado, então não foi possível
abri-la nos testes.

## Histórico de ajustes

| Ajuste | Arquivos |
| --- | --- |
| Versão inicial da página | todos |
| Botão flutuante de WhatsApp e links de WhatsApp em "Onde fica" e no rodapé | `index.html`, `assets/css/styles.css` |
| Remoção da legenda da foto do hero | `index.html`, `assets/css/styles.css` |
| Correção: a barra fixa do celular deixava de aparecer depois que o visitante passava pela seção do Clube | `assets/js/main.js` |

## Créditos e licenças

- Fotos, logo, avaliações e fotos de perfil: fornecidos pelo cliente.
- Archivo e Instrument Serif: SIL Open Font License 1.1, obtidas do Google
  Fonts e hospedadas localmente.
- Ícones: desenhados para este projeto. Ícone do WhatsApp: Simple Icons (CC0).

## Pendências que dependem do cliente

- Confirmar que o número (44) 99809-2162 atende por WhatsApp, já que o botão
  flutuante depende disso.
- Confirmar o sentido de "marca própria". Se for uma linha de produtos da
  Fialho, enviar nomes e fotos para uma seção dedicada.
- Conferir três afirmações sobre a agenda, que não puderam ser verificadas: ela
  funciona no celular e no computador, permite escolher serviço e horário, e
  traz a lista completa de serviços.
- Conferir os textos descritos a partir das fotos, em especial "Geladeira
  abastecida" e "Salão climatizado".
- Logo em vetor (SVG, AI ou PDF) ou em alta resolução.
- Fotos originais em alta resolução. Com as atuais, as imagens não podem
  ocupar mais que 440 px de largura.
- Domínio de publicação, para completar `og:image` com URL absoluta e adicionar
  `link rel="canonical"`.
- Horários de funcionamento e formas de pagamento.
- Dados do Clube Fialho (planos, valores e o que cada um inclui), caso se
  queira apresentá-los na própria página.
- Origem das avaliações (por exemplo, o link do perfil no Google), caso se
  queira citar a fonte, e autorização dos clientes para uso de nome e foto.
- Autorização de uso de imagem das pessoas que aparecem nas fotos, em especial
  a do menor de idade na seção de avaliações.
- Fotos de perfil das avaliações têm 72 x 72 px. Ficam nítidas no tamanho usado
  (48 px), mas não podem ser ampliadas.
