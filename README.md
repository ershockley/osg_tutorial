# osg_tutorial
Tutorial for using OSG, especially in context of XENON analysis


# Accounts and Logging in
To use OSG you need to have access to a submit node that has access to the grid. For XENON we have our own dedicated login node. 

First you need to get an account, see [wiki](https://xe1t-wiki.lngs.infn.it/doku.php?id=xenon:xenon1t:cmp:computing:midway_cluster:instructions) or go straight to CI-Connect site [here](https://www.ci-connect.net). Make sure to ask to join the `xenon1t` group when requesting your account. 

After setting up your account, you will need to add an ssh key to your profile to be able to login. 

Once that is all done, you should be able to access the machine:

```
ssh {username}@login.xenon.ci-connect.net
```

# Tutorial
This tutorial is split into multiple levels, with increasing complexity. 

A good place to start is the `hello_world` directory, which includes simple examples of just submitting simple bash scripts to OSG and working with arguments. 


