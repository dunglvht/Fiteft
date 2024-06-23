# ATLAS CONF 2020-053
The parametrization matrix $A[all]$, here all includes all the couplings:
<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/linearized.html>>
The Fisher information matrix of $[all]$ couplings:
$$
A_{[all]}^T V^{-1}A_{[all]}
$$
with
$$
V=V_{exp} = \Sigma(\mu).\rho.\Sigma(\mu)
$$
And the eigen vectors for such matrix matrix are
<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/eigen_vectors.html>>
If we cut the vectors with eigen values $<0.02$ we have [fig 05](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/CONFNOTES/ATLAS-CONF-2020-053/fig_05.pdf)
<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/eigen_vectors_partial.html>>

After we have choosed the specific combination of couplings to fit we will find the eigen vectors for such combinations
$$
A_{[c(3)Hq]}^T V^{-1}A_{[c(3)Hq]}
$$


<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/sub_vectors_0.html>>

$$
A_{[cHB,cHW,cHWB,cuB,cuW,cHDD]}^T V^{-1}A_{[cHB,cHW,cHWB,cuB,cuW,cHDD]}
$$

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/sub_vectors_1.html>>

$$
A_{[cHd, cHu,c(1)Hq]}^T V^{-1}A_{[cHd, cHu,c(1)Hq]}
$$

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/sub_vectors_2.html>>

$$
A_{[cHe,c(1)Hl]}^T V^{-1}A_{[cHe,c(1)Hl]}
$$

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/sub_vectors_3.html>>

$$
A_{[ c(3)Hl, c0ll]}^T V^{-1}A_{[ c(3)Hl, c0ll]}
$$

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/sub_vectors_4.html>>

$$
A_{ cHG, cuG, cG,c(8)qd, c(1)qq, cqq, c(3)qq, c(31)qq, c(1)qu, c(8)qu,cuH, c(8)ud, cuu, c(1)uu}^T V^{-1}A_{ cHG, cuG, cG,c(8)qd, c(1)qq, cqq, c(3)qq, c(31)qq, c(1)qu, c(8)qu,cuH, c(8)ud, cuu, c(1)uu}
$$

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/sub_vectors_5.html>>

And when combined, they look like this

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/sub_vectors.html>>

If we cut the vectors with eigenvalue $<0.4$, whe then have [fig 06](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/CONFNOTES/ATLAS-CONF-2020-053/fig_06.pdf)

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2020-053/latex/sub_vectors_partial.html>>

# ATLAS 2021-053

$$
V=V_{exp} +V_{theo}= \Sigma(y)_{exp}.\rho.\Sigma(y)_{exp} +\Sigma(y)_{th}.I.\Sigma(y)_{th}
$$
with
$$
\Sigma_{th} = \sqrt{\sigma_{th}^+\sigma_{th}^-(\sigma_{th}^+-\sigma_{th}^-)(y-\hat{y})}\\
\Sigma_{exp} = \sqrt{\sigma_{exp}^+\sigma_{exp}^-(\sigma_{exp}^+-\sigma_{exp}^-)(y-\hat{y})}
$$
From the above method, we can get

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2021-053/rotation/sub_vec_full.html>>

[fig 17](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/CONFNOTES/ATLAS-CONF-2021-053/fig_17.png)

<<file_name=C:/project/Fiteft/validation/ATLAS-CONF-2021-053/rotation/sub_vec_partial.html>>
