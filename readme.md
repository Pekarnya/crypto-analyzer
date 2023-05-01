# Decoupling the price action of the BTC/USDT from ETH/USDT
================================================================

>There are several methods of calculating correlation. The most common method, the Pearson product-moment correlation. 
>## The algorithm is based on the following assumptions

* Collecting the data from the coinmarket, through the API.
* Checking the correlation level
* Using the correlation level we can decouple the price action of the coin
* If the price action is changed 1% or higher, we get the message into the terminal

## Theory
------------------------

The Pearson (product-moment) correlation coefficient is a measure of the linear relationship between two features. It’s the ratio of the covariance of x and y to the product of their standard deviations. It’s often denoted with the letter r and called Pearson’s r. You can express this value mathematically with this equation:

r = Σᵢ((xᵢ − mean(x))(yᵢ − mean(y))) (√Σᵢ(xᵢ − mean(x))² √Σᵢ(yᵢ − mean(y))²)⁻¹

## License


## Contributors


## References

1. Bakar N. A., Rosbi S. Pearson product moment correlation diagnostics between two types of crypto-currencies: a case study of Bitcoin and Ethereum //International Journal of Advances in Scientific Research and Engineering. – 2018. – Т. 4. – №. 12. – С. 40-51.
2. Laskowski M., Kim H. M. Rapid prototyping of a text mining application for cryptocurrency market intelligence //2016 IEEE 17th International Conference on Information Reuse and Integration (IRI). – IEEE, 2016. – С. 448-453.
3. Demythifying the belief in cryptocurrencies decentralized aspects. A study of cryptocurrencies time cross-correlations with common currencies, commodities and financial indices
Author links open overlay panelSeyed Alireza Manavi a b 1, Gholamreza Jafari a 1, Shahin Rouhani b 1, Marcel Ausloos c d e 1
4. Exploring the Interconnectedness of Cryptocurrencies using Correlation Networks
Andrew Burnie
