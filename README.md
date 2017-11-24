# README #

Repositório contendo o protocolo de Disseminação de Dados baseado em Redes compleXas (DDRX) para Redes Veiculares Ad Hoc.

### Observações ###

* EM BREVE

### Executando ###

Acessar o diretório contendo o .ini do projeto:

	> cd ../workspace/DDRX/simulations

Executar a simulação de forma paralelizada com [GNU Parallel](https://www.gnu.org/software/parallel/):
	
	> parallel -j10 ../src/DDRX -r {1} -u Cmdenv -n .:../src:../../veins/examples/veins:../../veins/src/veins -l ../../veins/src/veins omnetpp.ini ::: {0..n}

Onde:

* -j é o número de núcleos que serão utilizados.
* ::: {0..n} é a quantidade de cenários multiplicado pela quantidade de seeds. Exemplo: 2 cenários com 10 seeds cada = {0..19} = 20 simulações.

Acompanhar os processos executando com o comando [htop](http://www.hardware.com.br/artigos/htop/):

	> htop -u nome_usuario

### Contato ###

* [Homepage UFPA](http://www.gercom2.ufpa.br/joahannes) || [Homepage UNICAMP](http://www.lrc.ic.unicamp.br/~joahannes)

### Colaboração ###

* Universidade Federal do Pará (UFPA)
* Universidade Estadual de Campinas (UNICAMP)
